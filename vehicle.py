#!/usr/bin/env python
from google.appengine.api import users
from flask import Flask, render_template, redirect, request
import datastore
import datetime
import models
import utils

app = Flask(__name__)

class ExpenseType():
    FUEL = 1
    MAINTENANCE = 2
    OTHER = 3

    @staticmethod
    def parse_page_name(page_name):
        if not page_name:
            return 0
        if page_name == "maintenance":
            return ExpenseType.MAINTENANCE
        elif page_name == "gasmileage":
            return ExpenseType.FUEL
        else:
            return ExpenseType.OTHER

def build_object(obj, expense_type, vehicle_id):
    context = utils.get_context()
    user_id = context['user']['userId']

    dateString = request.form.get("datePurchased", None)
    datePurchased = datetime.datetime.strptime(dateString, "%Y/%m/%d")
    location = request.form.get("location", "")
    amount = float(request.form.get("amount", None))
    description = request.form.get("description", "")
    category = request.form.get("category", "Uncategorized")

    if datePurchased and amount >= 0:
        categoryObj = None
        if expense_type != ExpenseType.FUEL:
            categoryObj = datastore.get_category_by_name(user_id, category, (expense_type == ExpenseType.MAINTENANCE))
            if not categoryObj:
                # this is a new category, add it to the database
                categoryObj = models.ExpenseCategory()
                categoryObj.owner = user_id
                if expense_type == ExpenseType.MAINTENANCE:
                    categoryObj.category = "Maintenance"
                    categoryObj.subcategory = category
                else:
                    categoryObj.category = category
                categoryObj.put()

        obj.owner = user_id
        obj.vehicle = long(vehicle_id)
        obj.date = datePurchased
        obj.location = location
        obj.description = description
        obj.amount = amount
        obj.lastmodified = datetime.datetime.now()

        if categoryObj:
            obj.categoryid = categoryObj.key.id()

    # Pass off record for more specific handling
    if expense_type == ExpenseType.FUEL:
        costPerGallon = float(request.form.get("pricepergallon", None))
        fuelGrade = request.form.get("grade")
        odometerStart = request.form.get("odometerStart", None)
        odometerEnd = request.form.get("odometerEnd", None)

        if odometerStart:
            odometerStart = int(odometerStart)
        else:
            odometerStart = -1

        if odometerEnd:
            odometerEnd = int(odometerEnd)
        else:
            odometerEnd = -1

        gallons = obj.amount / costPerGallon
        if odometerEnd != -1 and odometerStart != -1:
            mpg = (odometerEnd - odometerStart) / gallons
        else:
            mpg = -1

        if costPerGallon:
            obj.categoryid = datastore.get_category_by_name(user_id, "Fuel Up").key.id()
            obj.description = "Filled up with gas"
            obj.gallons = gallons
            obj.costPerGallon = costPerGallon
            obj.fuelGrade = fuelGrade
            obj.odometerStart = odometerStart
            obj.odometerEnd = odometerEnd
            obj.mpg = mpg
    elif expense_type == ExpenseType.MAINTENANCE:
        odometer = request.form.get("odometerEnd", None)
        if odometer:
            odometer = int(odometer)
        else:
            odometer = -1

        obj.odometer = odometer

    return obj

@app.route('/vehicle/<vehicle_id>/<page_name>/add', methods=['GET'])
def expense_add(vehicle_id, page_name):
    context = utils.get_context()
    user_id = context['user']['userId']

    if not vehicle_id:
        return redirect("/")
    else:
        page_type = ExpenseType.parse_page_name(page_name)
        context["car"] = datastore.get_user_vehicle(user_id, vehicle_id)

        if page_type == ExpenseType.FUEL:
            # Get latest fuel record
            latestFuel = datastore.get_n_fuel_records(user_id, vehicle_id, 1, False)
            if latestFuel and len(latestFuel) > 0:
                context["lastfuelrecord"] = latestFuel[0]

        if page_type == ExpenseType.MAINTENANCE:
            context["categories"] = datastore.get_maintenance_categories(user_id)
        else:
            context["categories"] = datastore.get_expense_categories(user_id)

        return render_template('addexpense.html', **context)

@app.route('/vehicle/<vehicle_id>/<page_name>/add', methods=['POST'])
def expense_add_post(vehicle_id, page_name):
    page_type = ExpenseType.parse_page_name(page_name)

    if page_type == ExpenseType.MAINTENANCE:
        expense = models.MaintenanceRecord()
    elif page_type == ExpenseType.FUEL:
        expense = models.FuelRecord()
    else:
        expense = models.UserExpenseRecord()

    obj = build_object(expense, page_type, vehicle_id)
    if obj:
        obj.put()

    # Redirect
    if page_type == ExpenseType.MAINTENANCE:
        return redirect("/vehicle/%s/maintenance" % vehicle_id)
    elif page_type == ExpenseType.FUEL:
        return redirect("/vehicle/%s/gasmileage" % vehicle_id)
    else:
        return redirect("/vehicle/%s/expenses" % vehicle_id)

@app.route('/vehicle/<vehicle_id>/<page_name>/edit/<expense_id>', methods=['GET'])
def expense_edit(vehicle_id, page_name, expense_id):
    context = utils.get_context()
    user_id = context['user']['userId']

    if not vehicle_id:
        return redirect("/")
    else:
        context["car"] = datastore.get_user_vehicle(user_id, vehicle_id)
        baseExpense = datastore.get_base_expense_record(user_id, vehicle_id, expense_id)

        # Perform redirection here if the expense is a specific type
        if baseExpense._class_name() == "MaintenanceRecord":
            context["editmaintenanceobj"] = baseExpense
            context["categories"] = datastore.get_maintenance_categories(user_id)
        elif baseExpense._class_name() == "FuelRecord":
            context["editfuelrecordobj"] = baseExpense
        else:
            context["editexpenseobj"] = baseExpense
            context["categories"] = datastore.get_expense_categories(user_id)

        category = datastore.get_category_by_id(user_id, baseExpense.categoryid)
        if not category:
            # This will make the category for this object become Uncategorized since old object is gone
            category = datastore.get_category_by_name(user_id, "Uncategorized")
            baseExpense.categoryid = category.key.id()

        baseExpense.categoryname = category.name()

        return render_template('addexpense.html', **context)

@app.route('/vehicle/<vehicle_id>/<page_name>/edit/<expense_id>', methods=['POST'])
def expense_edit_post(vehicle_id, page_name, expense_id):
    context = utils.get_context()
    user_id = context['user']['userId']
    if not expense_id:
        return redirect("/vehicle/%s/%s" % (vehicle_id, page_name))

    expense = datastore.get_base_expense_record(user_id, vehicle_id, expense_id)

    if expense._class_name() == "MaintenanceRecord":
        page_type = ExpenseType.MAINTENANCE
    elif expense._class_name() == "FuelRecord":
        page_type = ExpenseType.FUEL
    else:
        page_type = ExpenseType.OTHER

    obj = build_object(expense, page_type, vehicle_id)
    if obj:
        obj.put()

    # Redirect to the page that the user edited from
    return redirect("/vehicle/%s/%s" % (vehicle_id, page_name))

@app.route('/vehicle/<vehicle_id>/<page_name>/delete/<expense_id>')
def expense_delete(vehicle_id, page_name, expense_id):
    context = utils.get_context()
    user_id = context['user']['userId']
    page_type = ExpenseType.parse_page_name(page_name)

    if not vehicle_id:
        return redirect("/")
    elif not page_name:
        return redirect("/vehicle/%s" % vehicle_id)
    elif not expense_id:
        return redirect("/vehicle/%s/%s" % (vehicle_id, expense_id))
    else:
        # Delete record
        baseExpense = datastore.get_base_expense_record(user_id, vehicle_id, expense_id)
        datastore.delete_base_expense(user_id, baseExpense)

        # Redirect
        if page_type == ExpenseType.MAINTENANCE:
            return redirect("/vehicle/%s/maintenance" % vehicle_id)
        elif page_type == ExpenseType.FUEL:
            return redirect("/vehicle/%s/gasmileage" % vehicle_id)
        else:
            return redirect("/vehicle/%s/expenses" % vehicle_id)

@app.route('/vehicle/<vehicle_id>/expenses', methods=['GET'])
def expense(vehicle_id):
    context = utils.get_context()
    user_id = context['user']['userId']

    if not vehicle_id:
        return redirect("/")
    else:
        context["car"] = datastore.get_user_vehicle(user_id, vehicle_id)
        context["categories"] = datastore.get_expense_categories(user_id)
        context['userexpenses'] = datastore.get_all_expense_records(user_id, vehicle_id, 0, False)

        expenseTotal = 0
        for expense in context['userexpenses']:
            expenseTotal += expense.amount
            category = datastore.get_category_by_id(user_id, expense.categoryid)
            if not category:
                # This will make the category for this object become Uncategorized since old object is gone
                category = datastore.get_category_by_name(user_id, "Uncategorized")
                expense.categoryid = category.key.id()

            expense.categoryname = category.name()

        context['expensetotal'] = utils.format_float(expenseTotal)

        return render_template('expenses.html', **context)

@app.route('/vehicle/<vehicle_id>/maintenance', methods=['GET'])
def maintenance(vehicle_id):
    context = utils.get_context()
    user_id = context['user']['userId']

    if not vehicle_id:
        return redirect("/")
    else:
        context["car"] = datastore.get_user_vehicle(user_id, vehicle_id)
        context["categories"] = datastore.get_maintenance_categories(user_id)
        context["maintRecords"] = datastore.get_maintenance_records(user_id, vehicle_id, None)

        return render_template('maintenance.html', **context)

@app.route('/vehicle/<vehicle_id>/gasmileage', methods=['GET'])
def gas(vehicle_id):
    context = utils.get_context()
    user_id = context['user']['userId']

    if not vehicle_id:
        return redirect("/")
    else:
        context["car"] = datastore.get_user_vehicle(user_id, vehicle_id)
        context['userfuelrecords'] = datastore.get_fuel_records(user_id, vehicle_id, None, False)

        # add Average MPG as a comma-delimited string
        context['avgmpg'] = datastore.get_avg_gas_mileage(user_id, vehicle_id)

        # add milestotal as a comma-delimited string
        context['milestotal'] = datastore.get_total_miles(user_id, vehicle_id)
        context['pricepermile'] = datastore.get_cost_per_mile(user_id, vehicle_id)

        return render_template('gasmileage.html', **context)

@app.route('/vehicle', defaults={'vehicle_id': None, 'page_name': None}, methods=['GET'])
@app.route('/vehicle/<vehicle_id>', defaults={'page_name': None}, methods=['GET'])
@app.route('/vehicle/<vehicle_id>/<page_name>', methods=['GET'])
def vehicle(vehicle_id, page_name):
    context = utils.get_context()
    user_id = context['user']['userId']

    # If the path doesn't contain a first parameter, just show the garage
    if not vehicle_id:
        path = 'garage.html'

    # If we have a first path parameter, and it isn't add, use that as
    # the vehicle ID and show that vehicle's page
    else:
        context["car"] = datastore.get_user_vehicle(user_id, vehicle_id)
        context["latestMilage"] = utils.format_int(datastore.get_current_odometer(user_id, long(vehicle_id)))
        context["totalCost"] = utils.format_float(datastore.get_total_cost(user_id, long(vehicle_id)))

        if not context["car"]:
            return redirect("/")

        if page_name == "charts":
            path = 'charts.html'
        else:
            path = 'car.html'

    return render_template(path, **context)

@app.route('/vehicle/<make_option>/<model>', methods=['POST'])
def vehicle_post(make_option, model):
    context = utils.get_context()
    user_id = context['user']['userId']

    if make_option == "add":
        make = request.form.get("make", None)
        model = request.form.get("model", None)
        year = request.form.get("year", None)
        plates = request.form.get("licensePlates", None)
        color = request.form.get("color", None)

        if make and model and year:
            vehicle = models.UserVehicle()
            vehicle.make = make
            vehicle.model = model
            vehicle.year = year
            vehicle.color = color
            vehicle.plates = plates
            vehicle.owner = user_id
            vehicle.lastmodified = datetime.datetime.now()

            vehicle.put()
    elif model == "update":
        vehicle = datastore.get_user_vehicle(user_id, make_option)
        if vehicle:
            color = request.form.get("color", None)
            plates = request.form.get("plates", None)

            # Conditionally update the vehicle object
            vehicle.color = color if color else color.plates
            vehicle.plates = plates if plates else vehicle.plates

            vehicle.lastmodified = datetime.datetime.now()
            vehicle.put()

            return redirect("/vehicle/%d" % vehicle.key.id())

    elif model == "delete":
        datastore.delete_user_vehicle(user_id, make_option)

    return redirect("/")
