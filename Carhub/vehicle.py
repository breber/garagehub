#!/usr/bin/env python
from google.appengine.api import users
from google.appengine.ext.webapp import template
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
        context['userexpenses'] = datastore.getBaseExpenseRecords(user.user_id(), vehicleId, None, False) 
        
        expenseTotal = 0;
        for expense in  context['userexpenses']:
            expenseTotal += expense.amount
        
        context['expensetotal'] = expenseTotal
        
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
            
            # find out if new category has been added
            userCatgories = datastore.getUserExpenseCategories(currentUser.user_id())
            category = self.request.get("category", "Uncategorized")
            if not category in userCatgories:
                # this is a new category, add it to the database
                newCategoryObj = models.UserExpenseCategory()
                newCategoryObj.owner = currentUser.user_id()
                newCategoryObj.category = category
                newCategoryObj.put()

            location = self.request.get("location", "")
            amount = float(self.request.get("amount", None))
            description = self.request.get("description", "")
            logging.info("Expense Info Obtained %s %s %s %s %d", datePurchased, category, location, description, amount)
            
            if datePurchased and amount:
                logging.info("Expense Being Added")
                expense = models.BaseExpense()
                expense.date = datePurchased
                expense.category = category
                expense.location = location
                expense.amount = amount
                expense.description = description
                
                #TODO: get image for receipt
                
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
                category = self.request.get("category", "Uncategorized")

            location = self.request.get("location", "")
            amount = float(self.request.get("amount", None))
            description = self.request.get("description", "")
            odometer = self.request.get("odometer",None)
            if odometer:
                odometer = int(odometer)
            else:
                odometer = -1
            logging.info("Maintenance Info Obtained %s %s %s %s %f %d", datePurchased, category, location, description, amount, odometer)
            
            if datePurchased and amount:
                maintRec = models.MaintenanceRecord()
                maintRec.date = datePurchased
                maintRec.category = category
                maintRec.location = location
                maintRec.amount = amount
                maintRec.description = description
                maintRec.odometer = odometer
                
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
        context['userfuelrecords'] = datastore.getFuelRecords(user.user_id(), vehicleId, None, False)
        latestFuel = datastore.getNFuelRecords(user.user_id(), vehicleId, 1, False)
        if latestFuel and len(latestFuel) > 0:
            context["lastfuelrecord"] = latestFuel[0]
        
        if not vehicleId:
            self.redirect("/")
        else:
            if pageName == "add":
                path = os.path.join(os.path.dirname(__file__), 'templates/addexpense.html')
            else:
                path = os.path.join(os.path.dirname(__file__), 'templates/gasmileage.html')
                
            self.response.out.write(template.render(path, context))
    
    def post(self, vehicleId, model):
        
        #TODO: handle what to do if the optional fields are not entered.
        currentUser = users.get_current_user()
        
        logging.info("entered the Gas Mileage Expense post function")
        
        if currentUser:
            dateString = self.request.get("datePurchased", None)
            datePurchased = datetime.datetime.strptime(dateString, "%Y-%m-%d")

            location = self.request.get("location", "")
            amount = float(self.request.get("amount", None))
            costPerGallon = float(self.request.get("pricepergallons", None))
            fuelGrade = self.request.get("grade")
            
            # try to get from last fuel record if user wants to, or else try to get it from 
            #      the manual entry tab if it is not entered then assume it is -1 which means N/A
            useOdometerLastRecord = self.request.get("sinceLastFuelRecord",False)
            
            lastFuelRecord = None
            if useOdometerLastRecord:
                # find the previous gas record and grab the odometer reading
                latestFuel = datastore.getNFuelRecords(currentUser.user_id(), vehicleId, 1, False)
                if latestFuel and len(latestFuel) > 0:
                    lastFuelRecord = latestFuel[0]
                    odometerStart = lastFuelRecord.odometerEnd
            if not lastFuelRecord:
                # try to get from manual odometer start entry
                odometerStart = self.request.get("odometerStart",None)
                if odometerStart and odometerStart != "Enter Odometer Start":
                    odometerStart = int(odometerStart)
                else:
                    odometerStart = -1
            
            
            odometerEnd = self.request.get("odometerEnd",None)
            if odometerEnd:
                odometerEnd = int(odometerEnd)
            else:
                odometerEnd = -1
            
            gallons = amount / costPerGallon
            if odometerEnd != -1 and odometerStart != -1:
                mpg = (odometerEnd - odometerStart)/gallons
            else:
                mpg = -1;
                    
            logging.info("Expense Info Obtained %s %s %d %d %d %d", datePurchased, location, amount, costPerGallon, odometerStart, odometerEnd)
            
            if datePurchased and amount and costPerGallon:
                record = models.FuelRecord()
                record.date = datePurchased
                #TODO: this is the category for all Fuel Records, move to a constants file
                record.category = "Fuel Record"
                record.location = location
                record.amount = amount
                #TODO: this is the description for all fuel records, move to a constants file
                record.description = "Filled up with gas"
                record.gallons = gallons
                record.costPerGallon = costPerGallon
                record.fuelGrade = fuelGrade 
                record.odometerStart = odometerStart
                record.odometerEnd = odometerEnd
                record.mpg = mpg
                
                # record ownership
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
            context["latestMilage"] = datastore.getLastRecordedMileage(currentUserId, long(vehicleId))
            context["totalCost"] = datastore.getTotalCost(currentUserId, long(vehicleId))
            
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
