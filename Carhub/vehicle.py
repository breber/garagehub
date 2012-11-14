#!/usr/bin/env python
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from models import FuelRecord
import datastore
import datetime
import logging
import models
import os
import utils
import webapp2

class VehicleExpenseHandler(webapp2.RequestHandler):
    def get(self, vehicleId, pageName):
        context = utils.get_context()
        user = users.get_current_user()
        context["car"] = datastore.getUserVehicle(user.user_id(), vehicleId)
        context["categories"] = datastore.getUserExpenseCategories(user.user_id())
        context['userexpenses'] = datastore.getBaseExpenseRecords(user.user_id(), vehicleId, 30) 
        
        if not vehicleId:
            self.redirect("/")
        else:
            if pageName == "add":
                path = os.path.join(os.path.dirname(__file__), 'templates/addexpense.html')
            else:
                path = os.path.join(os.path.dirname(__file__), 'templates/expenses.html')
                
            self.response.out.write(template.render(path, context))
    
    def post(self, vehicleId, model):
        currentUser = users.get_current_user()
        
        logging.info("entered the Expense post function")
        
        if currentUser:
            dateString = self.request.get("datePurchased", None)
            datePurchased = datetime.datetime.strptime(dateString, "%Y-%m-%d")
            newCategory = self.request.get("newCategory", None)
            
            if newCategory:
                category = newCategory
                newCategoryObj = models.UserExpenseCategory()
                newCategoryObj.owner = currentUser.user_id()
                newCategoryObj.category = newCategory

                if not newCategoryObj.category in datastore.getUserExpenseCategories(currentUser.user_id()):
                    newCategoryObj.put()

            else:
                category = self.request.get("category", None)
                
                # if no category selected then default to uncategorized
                if (category == "Select a Category"):
                    category = "Uncategorized"

            location = self.request.get("location", None)
            amount = float(self.request.get("amount", None))
            description = self.request.get("description", None)
            logging.info("Expense Info Obtained %s %s %s %s %d", datePurchased, category, location, description, amount)
            
            if datePurchased and category and location and amount and description:
                expense = models.BaseExpense()
                expense.date = datePurchased
                expense.category = category
                expense.location = location
                expense.amount = amount
                expense.description = description
                
                #TODO get image for receipt
                
                expense.owner = currentUser.user_id()
                expense.vehicle = long(vehicleId)
                expense.lastmodified = datetime.datetime.now()
                
                expense.put()

        self.redirect("/vehicle/%s/expenses" % vehicleId)     
        
        
class VehicleMaintenanceHandler(webapp2.RequestHandler):
    def get(self, vehicleId, pageName):
        context = utils.get_context()
        user = users.get_current_user()
        
        if not vehicleId:
            path = os.path.join(os.path.dirname(__file__), 'templates/garage.html')
            self.response.out.write(template.render(path, context))
        else:
            context["car"] = datastore.getUserVehicle(user.user_id(), vehicleId)
            categories = datastore.getMaintenanceCategories(user.user_id())
            if len(categories) > 0:
                context["categories"] = categories
            
            if pageName == "add":
                path = os.path.join(os.path.dirname(__file__), 'templates/addexpense.html')
            else:
                path = os.path.join(os.path.dirname(__file__), 'templates/maintenance.html')
            
                maintRecords = datastore.getMaintenanceRecords(user.user_id(), vehicleId)
            
                if len(maintRecords) > 0:
                    context["maintRecords"] = maintRecords
                
            self.response.out.write(template.render(path, context))
    
    def post(self, vehicleId, model):
        
        # TODO: Validation
        currentUser = users.get_current_user()
        
        logging.info("entered the Maintenance Expense post function")
        
        if currentUser:
            dateString = self.request.get("datePurchased", None)
            datePurchased = datetime.datetime.strptime(dateString, "%Y-%m-%d")
            
            #check to see if a new category is being used
            newCategory = self.request.get("newCategory", None)
            
            if newCategory:
                category = newCategory
                newCategoryObj = models.MaintenanceCategory()
                newCategoryObj.owner = currentUser.user_id()
                newCategoryObj.category = newCategory

                if not newCategoryObj.category in datastore.getMaintenanceCategories(currentUser.user_id()):
                    newCategoryObj.put()

            else:
                # Not using a new category, so get the existing category
                category = self.request.get("category", None)
                
                # if no category selected then default to uncategorized
                if (category == "Select a Category"):
                    category = "Uncategorized"

            location = self.request.get("location", None)
            amount = float(self.request.get("amount", None))
            description = self.request.get("description", None)
            odometer = int(self.request.get("odometer", None))
            logging.info("Maintenance Info Obtained %s %s %s %s %f %d", datePurchased, category, location, description, amount, odometer)
            
            if datePurchased and category and location and amount and description:
                maintRec = models.MaintenanceRecord()
                maintRec.date = datePurchased
                maintRec.category = category
                maintRec.location = location
                maintRec.amount = amount
                maintRec.description = description
                
                odometer = self.request.get("odometer", None)
                if odometer:
                    maintRec.odometer = int(odometer)
                
                maintRec.owner = currentUser.user_id()
                maintRec.vehicle = long(vehicleId)
                maintRec.lastmodified = datetime.datetime.now()
                
                maintRec.put()

        self.redirect("/vehicle/%s/maintenance" % vehicleId)

class VehicleGasMileageHandler(webapp2.RequestHandler):
    def get(self, vehicleId, pageName):
        context = utils.get_context()
        user = users.get_current_user()
        context["car"] = datastore.getUserVehicle(user.user_id(), vehicleId)
        context["categories"] = datastore.getUserExpenseCategories(user.user_id())
        context['userfuelrecords'] = datastore.getFuelRecords(user.user_id(), vehicleId, 30) 
        
        if not vehicleId:
            self.redirect("/")
        else:
            if pageName == "add":
                path = os.path.join(os.path.dirname(__file__), 'templates/addexpense.html')
            else:
                path = os.path.join(os.path.dirname(__file__), 'templates/gasmileage.html')
                
            self.response.out.write(template.render(path, context))
    
    def post(self, vehicleId, model):
        
        #TODO make this accept a Gas Mileage object
        
        #TODO handle what to do if the optional fields are not entered.
        currentUser = users.get_current_user()
        
        logging.info("entered the Gas Mileage Expense post function")
        
        if currentUser:
            dateString = self.request.get("datePurchased", None)
            datePurchased = datetime.datetime.strptime(dateString, "%m/%d/%Y")
            newCategory = self.request.get("newCategory", None)
            
            if newCategory:
                category = newCategory
                newCategoryObj = models.UserExpenseCategory()
                newCategoryObj.owner = currentUser.user_id()
                newCategoryObj.category = newCategory

                if not newCategoryObj.category in datastore.getUserExpenseCategories(currentUser.user_id()):
                    newCategoryObj.put()

            else:
                category = self.request.get("category", None)

            location = self.request.get("location", None)
            amount = float(self.request.get("amount", None))
            description = self.request.get("description", None)
            odometer = int(self.request.get("odometer". None))
            costPerGallon = float(self.request.get("pricepergallons", None))
            fuelGrade = self.request.get("grade")
            
            gallons = amount / costPerGallon
            logging.info("Expense Info Obtained %s %s %s %s %d", datePurchased, category, location, description, amount)
            
            if datePurchased and category and location and amount and description:
                record = models.FuelRecord()
                record.date = datePurchased
                #TODO this is the category for all Fuel Records, move to a constants file
                record.category = "Fuel Record"
                record.location = location
                record.amount = amount
                #TODO this is the description for all fuel records
                record.description = "Filled up with gas"
                record.odometerEnd = odometer
                
                lastFuelRecord = 0
                # find the previous gas record and grab the odometer reading
                for fuelRecord in  datastore.getFuelRecords(currentUser.user_id(), vehicleId, 30):
                    if not lastFuelRecord:
                        lastFuelRecord = fuelRecord
                    elif(lastFuelRecord.date < FuelRecord.date):
                        lastFuelRecord = fuelRecord
                
                if lastFuelRecord:
                    record.odometerStart = lastFuelRecord.odometerEnd
                else:
                    #TODO don't know how to handle this
                    record.odometerStart = -1
                    
                record.gallons = gallons
                record.costPerGallon = costPerGallon
                record.fuelGrade = fuelGrade                
                
                record.owner = currentUser.user_id()
                record.vehicle = long(vehicleId)
                record.lastmodified = datetime.datetime.now()
                
                record.put()

        self.redirect("/vehicle/%s/gasmileage" % vehicleId)



class VehicleHandler(webapp2.RequestHandler):
    def get(self, vehicleId, pageName):
        context = utils.get_context()
        currentUserId = users.get_current_user().user_id()
        
        # If the path doesn't contain a first parameter, just show the garage
        if not vehicleId:
            path = os.path.join(os.path.dirname(__file__), 'templates/garage.html')
            self.response.out.write(template.render(path, context))
            
        # If the first path parameter is "add", show the add vehicle page 
        elif vehicleId == "add":
            context["vehicles"] = datastore.getListOfMakes()
            
            path = os.path.join(os.path.dirname(__file__), 'templates/addvehicle.html')
            self.response.out.write(template.render(path, context))
        
        # If we have a first path parameter, and it isn't add, use that as
        # the vehicle ID and show that vehicle's page
        else:
            context["car"] = datastore.getUserVehicle(currentUserId, vehicleId)
            latestFuel = datastore.getNFuelRecords(currentUserId, vehicleId, 1)
            if latestFuel and len(latestFuel) > 0:
                context["fuel"] = latestFuel[0]
            
            # TODO: add total expense to the output
            
            if not context["car"]:
                self.redirect("/")
            
            if pageName == "charts":
                path = os.path.join(os.path.dirname(__file__), 'templates/charts.html')
            elif pageName == "news":
                path = os.path.join(os.path.dirname(__file__), 'templates/news.html')
            elif pageName == "addrecord":
                path = os.path.join(os.path.dirname(__file__), 'templates/addrecord.html')
            else:
                path = os.path.join(os.path.dirname(__file__), 'templates/car.html')
                
            self.response.out.write(template.render(path, context))
    
    def post(self, makeOption, model):
        currentUser = users.get_current_user()

        if currentUser:
            if makeOption == "add":
                make = self.request.get("make", None)
                model = self.request.get("model", None)
                year = self.request.get("year", None)
                
                if make and model and year:
                    vehicle = models.UserVehicle()
                    vehicle.make = make
                    vehicle.model = model
                    vehicle.year = year
                    vehicle.owner = currentUser.user_id()
                    vehicle.lastmodified = datetime.datetime.now()
                    
                    vehicle.put()
            elif model == "update":
                vehicle = datastore.getUserVehicle(currentUser.user_id(), makeOption)
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
                vehicle = datastore.getUserVehicle(currentUser.user_id(), makeOption)
                if vehicle:
                    # TODO: delete all data that corresponds to this vehicle
                    vehicle.key.delete()
            
        self.redirect("/")
        
app = webapp2.WSGIApplication([                  
    ('/vehicle/([^/]+)/expenses/?(.+?)?', VehicleExpenseHandler),
    ('/vehicle/([^/]+)/maintenance/?(.+?)?', VehicleMaintenanceHandler),
    ('/vehicle/([^/]+)/gasmileage/?(.+?)?', VehicleGasMileageHandler),
    ('/vehicle/([^/]+)?/?(.+?)?', VehicleHandler),
], debug=True)
