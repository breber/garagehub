#!/usr/bin/env python
from google.appengine.ext.webapp import template
from google.appengine.api import users
import datastore
import json
import os
import utils
import webapp2
import models

class MainHandler(webapp2.RequestHandler):
    def get(self):
        context = utils.get_context()
        
        path = os.path.join(os.path.dirname(__file__), 'templates/home.html')
        self.response.out.write(template.render(path, context))

class RawVehicleHandler(webapp2.RequestHandler):
    def get(self, make, model):
        self.response.headerlist = [('Content-type', 'application/json')]
        
        if not model:
            modelList = datastore.getListOfModels(make)
            self.response.out.write(json.dumps(modelList))
        else:
            yearList = datastore.getListOfYears(make, model)
            self.response.out.write(json.dumps(yearList))

class VehicleHandler(webapp2.RequestHandler):
    def get(self, makeOption, model):
        context = utils.get_context()
        
        if not makeOption:
            # TODO: template should be garage
            path = os.path.join(os.path.dirname(__file__), 'templates/addvehicle.html')
            self.response.out.write(template.render(path, context))
        elif makeOption == "add":
            context["vehicles"] = datastore.getListOfMakes()
            
            path = os.path.join(os.path.dirname(__file__), 'templates/addvehicle.html')
            self.response.out.write(template.render(path, context))
        else:
            # TODO: should be vehicle page
            path = os.path.join(os.path.dirname(__file__), 'templates/addvehicle.html')
            self.response.out.write(template.render(path, context))
    
    def post(self, makeOption, model):
        currentUser = users.get_current_user()
        
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
                
                vehicle.put()
            
        self.redirect("/")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/vehicle/([^/]+)?/?(.+?)?', VehicleHandler),
    ('/cars/raw/([^/]+)?/?(.+?)?', RawVehicleHandler)
], debug=True)
