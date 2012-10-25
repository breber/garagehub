#!/usr/bin/env python
from google.appengine.api import users
from google.appengine.ext.webapp import template
import datastore
import datetime
import json
import models
import logging
import os
import utils
import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        context = utils.get_context()
        
        if users.get_current_user():
            path = os.path.join(os.path.dirname(__file__), 'templates/garage.html')
        else:
            path = os.path.join(os.path.dirname(__file__), 'templates/welcome.html')
            
        self.response.out.write(template.render(path, context))

class SettingsHandler(webapp2.RequestHandler):
    def get(self):
        context = utils.get_context()
        
        if users.get_current_user():
            path = os.path.join(os.path.dirname(__file__), 'templates/settings.html')
            self.response.out.write(template.render(path, context))
        else:
            self.redirect("/")

class RawVehicleHandler(webapp2.RequestHandler):
    def get(self, make, model):
        self.response.headerlist = [('Content-type', 'application/json')]
        
        if not model:
            modelList = datastore.getListOfModels(make)
            self.response.out.write(json.dumps(modelList))
        else:
            yearList = datastore.getListOfYears(make, model)
            self.response.out.write(json.dumps(yearList))

class VehicleExpenseHandler(webapp2.RequestHandler):
    def get(self, vehicleId, pageName):
        context = utils.get_context()
        context["car"] = datastore.getUserVehicle(vehicleId)
        
        if not vehicleId:
            self.redirect("/")
        else:
            if pageName == "add":
                path = os.path.join(os.path.dirname(__file__), 'templates/addexpense.html')
            else:
                path = os.path.join(os.path.dirname(__file__), 'templates/expenses.html')
                
            self.response.out.write(template.render(path, context))
    
    def post(self, makeOption, model):
        currentUser = users.get_current_user()
        
        logging.info("entered the post function")
        
        if currentUser:
#            TODO: do something with the post
            datePurchased = self.request.get("datePurchased", None)
            category = self.request.get("category", None)
            location = self.request.get("location", None)
            amount = self.request.get("amount", None)
            description = self.request.get("description", None)
            logging.info("I finished getting information")
            logging.info("%s %s %s %s %d" % datePurchased, category, location, description, amount)
            
            if datePurchased and category and location and amount and description:
                expense = models.UserExpense()
                expense.purchaseDate = datePurchased
                expense.category = category
                expense.location = location
                expense.amount = amount
                expense.description = description
                
                expense.owner = currentUser.user_id()
                expense.vehicle = "Fake Car TODO" #TODO
                expense.lastmodified = datetime.datetime.now()
                
                expense.put()
            
            
        self.redirect("/")

class VehicleHandler(webapp2.RequestHandler):
    def get(self, vehicleId, pageName):
        context = utils.get_context()
        
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
            context["car"] = datastore.getUserVehicle(vehicleId)
                
            if pageName == "maintenance":
                path = os.path.join(os.path.dirname(__file__), 'templates/maintenance.html')
            elif pageName == "gasmileage":
                path = os.path.join(os.path.dirname(__file__), 'templates/gasmileage.html')
            elif pageName == "charts":
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
        
        logging.info("entered the add vehicle post function")
        
        if currentUser:
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
            
        self.redirect("/")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/settings', SettingsHandler),
    ('/vehicle/([^/]+)/expenses/?(.+?)?', VehicleExpenseHandler),
    ('/vehicle/([^/]+)?/?(.+?)?', VehicleHandler),
    ('/cars/raw/([^/]+)?/?(.+?)?', RawVehicleHandler)
], debug=True)
