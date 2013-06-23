#!/usr/bin/env python
from google.appengine.api import images, users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers, template
import datastore
import datetime
import models
import os
import utils
import webapp2

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

def build_object(request, obj, expense_type, vehicle_id):
    context = utils.get_context()
    user_id = context['user']['userId']

    fileChosen = request.request.get("file", None)
    recieptKey = None
    imageUrl = None
    if fileChosen:
        upload_files = request.get_uploads('file')
        if len(upload_files) > 0:
            blob_info = upload_files[0]
            recieptKey = str(blob_info.key())
            imageUrl = images.get_serving_url(blob_info.key(), 400)

    dateString = request.request.get("datePurchased", None)
    datePurchased = datetime.datetime.strptime(dateString, "%Y/%m/%d")
    location = request.request.get("location", "")
    amount = float(request.request.get("amount", None))
    description = request.request.get("description", "")
    category = request.request.get("category", "Uncategorized")

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

        # This ensures that editing a record won't delete the picture
        if recieptKey:
            oldImage = obj.picture
            if oldImage:  # delete old picture
                images.delete_serving_url(oldImage)
                blobstore.BlobInfo.get(oldImage).delete()
            obj.picture = recieptKey
            obj.pictureurl = imageUrl

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
        VehicleGasMileageHandler.handle_request(request, user_id, obj)
    elif expense_type == ExpenseType.MAINTENANCE:
        VehicleMaintenanceHandler.handle_request(request, user_id, obj)
    else:
        VehicleExpenseHandler.handle_request(request, user_id, obj)

    return obj

class VehicleExpenseAddHandler(blobstore_handlers.BlobstoreUploadHandler):
    def get(self, vehicle_id, page_name):
        context = utils.get_context()
        user_id = context['user']['userId']

        if not vehicle_id:
            self.redirect("/")
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
            context["upload_url"] = blobstore.create_upload_url(self.request.url)

            path = os.path.join(os.path.dirname(__file__), 'templates/addexpense.html')
            self.response.out.write(template.render(path, context))

    def post(self, vehicle_id, page_name):
        page_type = ExpenseType.parse_page_name(page_name)

        if page_type == ExpenseType.MAINTENANCE:
            expense = models.MaintenanceRecord()
        elif page_type == ExpenseType.FUEL:
            expense = models.FuelRecord()
        else:
            expense = models.BaseExpense()

        obj = build_object(self, expense, page_type, vehicle_id)
        if obj:
            obj.put()

        # Redirect
        if page_type == ExpenseType.MAINTENANCE:
            self.redirect("/vehicle/%s/maintenance" % vehicle_id)
        elif page_type == ExpenseType.FUEL:
            self.redirect("/vehicle/%s/gasmileage" % vehicle_id)
        else:
            self.redirect("/vehicle/%s/expenses" % vehicle_id)


class VehicleExpenseEditHandler(blobstore_handlers.BlobstoreUploadHandler):
    def get(self, vehicle_id, page_name, expense_id):
        context = utils.get_context()
        user_id = context['user']['userId']

        if not vehicle_id:
            self.redirect("/")
        else:
            context["car"] = datastore.get_user_vehicle(user_id, vehicle_id)
            context["upload_url"] = blobstore.create_upload_url(self.request.url)
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

            path = os.path.join(os.path.dirname(__file__), 'templates/addexpense.html')
            self.response.out.write(template.render(path, context))

    def post(self, vehicle_id, page_name, expense_id):
        context = utils.get_context()
        user_id = context['user']['userId']
        if not expense_id:
            self.redirect("/vehicle/%s/%s" % (vehicle_id, page_name))
            return

        expense = datastore.get_base_expense_record(user_id, vehicle_id, expense_id)

        if expense._class_name() == "MaintenanceRecord":
            page_type = ExpenseType.MAINTENANCE
        elif expense._class_name() == "FuelRecord":
            page_type = ExpenseType.FUEL
        else:
            page_type = ExpenseType.OTHER

        obj = build_object(self, expense, page_type, vehicle_id)
        if obj:
            obj.put()

        # Redirect to the page that the user edited from
        self.redirect("/vehicle/%s/%s" % (vehicle_id, page_name))

class VehicleExpenseDeleteHandler(webapp2.RequestHandler):
    def get(self, vehicle_id, page_name, expense_id):
        context = utils.get_context()
        user_id = context['user']['userId']
        page_type = ExpenseType.parse_page_name(page_name)

        if not vehicle_id:
            self.redirect("/")
        elif not page_name:
            self.redirect("/vehicle/%s" % vehicle_id)
        elif not expense_id:
            self.redirect("/vehicle/%s/%s" % (vehicle_id, expense_id))
        else:
            # Delete record
            baseExpense = datastore.get_base_expense_record(user_id, vehicle_id, expense_id)
            datastore.delete_base_expense(user_id, baseExpense)

            # Redirect
            if page_type == ExpenseType.MAINTENANCE:
                self.redirect("/vehicle/%s/maintenance" % vehicle_id)
            elif page_type == ExpenseType.FUEL:
                self.redirect("/vehicle/%s/gasmileage" % vehicle_id)
            else:
                self.redirect("/vehicle/%s/expenses" % vehicle_id)

class VehicleExpenseHandler(webapp2.RequestHandler):
    def get(self, vehicle_id):
        context = utils.get_context()
        user_id = context['user']['userId']

        if not vehicle_id:
            self.redirect("/")
        else:
            context["car"] = datastore.get_user_vehicle(user_id, vehicle_id)
            context["categories"] = datastore.get_expense_categories(user_id)
            context['userexpenses'] = datastore.get_all_expense_records(user_id, vehicle_id, 0, False)

            expenseTotal = 0;
            for expense in context['userexpenses']:
                expenseTotal += expense.amount
                category = datastore.get_category_by_id(user_id, expense.categoryid)
                if not category:
                    # This will make the category for this object become Uncategorized since old object is gone
                    category = datastore.get_category_by_name(user_id, "Uncategorized")
                    expense.categoryid = category.key.id()

                expense.categoryname = category.name()

            context['expensetotal'] = utils.format_float(expenseTotal)

            path = os.path.join(os.path.dirname(__file__), 'templates/expenses.html')

            self.response.out.write(template.render(path, context))

    @staticmethod
    def handle_request(request, user_id, obj):
        # Nothing to do...
        return

class VehicleMaintenanceHandler(webapp2.RequestHandler):
    def get(self, vehicle_id):
        context = utils.get_context()
        user_id = context['user']['userId']

        if not vehicle_id:
            self.redirect("/")
        else:
            context["car"] = datastore.get_user_vehicle(user_id, vehicle_id)
            context["categories"] = datastore.get_maintenance_categories(user_id)
            context["maintRecords"] = datastore.get_maintenance_records(user_id, vehicle_id, None)

            path = os.path.join(os.path.dirname(__file__), 'templates/maintenance.html')
            self.response.out.write(template.render(path, context))

    @staticmethod
    def handle_request(request, user_id, obj):
        odometer = request.request.get("odometerEnd", None)
        if odometer:
            odometer = int(odometer)
        else:
            odometer = -1

        obj.odometer = odometer

        # Notification stuff
        # TODO: rework the category stuff here...
        category = datastore.get_category_by_id(user_id, obj.categoryid)
        relevantNotif = datastore.get_notification(user_id, long(obj.vehicle), category.category, None)
        if relevantNotif:
            lastMaintRec = datastore.get_n_maint_records(user_id, long(obj.vehicle), category.category, 1)

            if obj.date == lastMaintRec.date:
                if relevantNotif.recurring:
                    if relevantNotif.dateBased:
                        recurringMonths = lastMaintRec.recurringMonths
                        lastRecordedDate = lastMaintRec.date
                        yearDecimalNum = lastRecordedDate.strftime("%Y")
                        monthDecimalNum = lastRecordedDate.strftime("%m")
                        notifyYear = int(yearDecimalNum) + recurringMonths / 12
                        notifyMonth = int(monthDecimalNum) + (recurringMonths % 12)
                        if notifyMonth > 12:
                            notifyMonth -= 12
                            notifyYear += 1
                        relevantNotif.date = datetime.date(notifyYear, notifyMonth, lastRecordedDate.day)
                    if relevantNotif.mileBased:
                        relevantNotif.mileage = lastMaintRec.odometer + relevantNotif.recurringMiles
                    deltaoneday = datetime.timedelta(days=1)
                    relevantNotif.dateLastSeen = datetime.date.today() - deltaoneday
                    relevantNotif.put()
                else:
                    relevantNotif.key.delete()

class VehicleGasMileageHandler(webapp2.RequestHandler):
    def get(self, vehicle_id):
        context = utils.get_context()
        user_id = context['user']['userId']

        if not vehicle_id:
            self.redirect("/")
        else:
            context["car"] = datastore.get_user_vehicle(user_id, vehicle_id)
            context['userfuelrecords'] = datastore.get_fuel_records(user_id, vehicle_id, None, False)

            # add Average MPG as a comma-delimited string
            context['avgmpg'] = datastore.get_avg_gas_mileage(user_id, vehicle_id)

            # add milestotal as a comma-delimited string
            context['milestotal'] = datastore.get_total_miles(user_id, vehicle_id)
            context['pricepermile'] = datastore.get_cost_per_mile(user_id, vehicle_id)
            path = os.path.join(os.path.dirname(__file__), 'templates/gasmileage.html')

            self.response.out.write(template.render(path, context))

    @staticmethod
    def handle_request(request, user_id, obj):
        costPerGallon = float(request.request.get("pricepergallon", None))
        fuelGrade = request.request.get("grade")
        useOdometerLastRecord = request.request.get("sinceLastFuelRecord", False)
        odometerEnd = request.request.get("odometerEnd", None)

        lastFuelRecord = None
        if useOdometerLastRecord:
            # find the previous gas record and grab the odometer reading
            latestFuel = datastore.get_n_fuel_records(user_id, obj.vehicle, 1, False)
            if latestFuel and len(latestFuel) > 0:
                lastFuelRecord = latestFuel[0]
                odometerStart = lastFuelRecord.odometerEnd
        if not lastFuelRecord:
            # try to get from manual odometer start entry
            odometerStart = request.request.get("odometerStart", None)
            if odometerStart and odometerStart != "Enter Odometer Start":
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
            mpg = -1;

        if costPerGallon:
            obj.categoryid = datastore.get_category_by_name(user_id, "Fuel Up").key.id()
            obj.description = "Filled up with gas"
            obj.gallons = gallons
            obj.costPerGallon = costPerGallon
            obj.fuelGrade = fuelGrade
            obj.odometerStart = odometerStart
            obj.odometerEnd = odometerEnd
            obj.mpg = mpg


class VehicleHandler(webapp2.RequestHandler):
    def get(self, vehicle_id, page_name):
        context = utils.get_context()
        user_id = context['user']['userId']

        # If the path doesn't contain a first parameter, just show the garage
        if not vehicle_id:
            path = os.path.join(os.path.dirname(__file__), 'templates/garage.html')

        # If we have a first path parameter, and it isn't add, use that as
        # the vehicle ID and show that vehicle's page
        else:
            context["car"] = datastore.get_user_vehicle(user_id, vehicle_id)
            context["latestMilage"] = utils.format_int(datastore.get_current_odometer(user_id, long(vehicle_id)))
            context["totalCost"] = utils.format_float(datastore.get_total_cost(user_id, long(vehicle_id)))

            if not context["car"]:
                self.redirect("/")

            if page_name == "charts":
                path = os.path.join(os.path.dirname(__file__), 'templates/charts.html')
            elif page_name == "news":
                path = os.path.join(os.path.dirname(__file__), 'templates/news.html')
            else:
                path = os.path.join(os.path.dirname(__file__), 'templates/car.html')

        self.response.out.write(template.render(path, context))

    def post(self, make_option, model):
        context = utils.get_context()
        user_id = context['user']['userId']

        if make_option == "add":
            make = self.request.get("make", None)
            model = self.request.get("model", None)
            year = self.request.get("year", None)
            plates = self.request.get("licensePlates", None)
            color = self.request.get("color", None)

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
                color = self.request.get("color", None)
                plates = self.request.get("plates", None)

                # Conditionally update the vehicle object
                vehicle.color = color if color else color.plates
                vehicle.plates = plates if plates else vehicle.plates

                vehicle.lastmodified = datetime.datetime.now()
                vehicle.put()

                self.redirect("/vehicle/%d" % vehicle.key.id())
                return

        elif model == "delete":
            datastore.delete_user_vehicle(user_id, make_option)

        self.redirect("/")

app = webapp2.WSGIApplication([
    ('/vehicle/([^/]+)/([^/]+)/add', VehicleExpenseAddHandler),
    ('/vehicle/([^/]+)/([^/]+)/edit/([^/]+)', VehicleExpenseEditHandler),
    ('/vehicle/([^/]+)/([^/]+)/delete/([^/]+)', VehicleExpenseDeleteHandler),

    ('/vehicle/([^/]+)/expenses', VehicleExpenseHandler),
    ('/vehicle/([^/]+)/maintenance', VehicleMaintenanceHandler),
    ('/vehicle/([^/]+)/gasmileage', VehicleGasMileageHandler),
    ('/vehicle/([^/]+)?/?(.+?)?', VehicleHandler),
], debug=True)
