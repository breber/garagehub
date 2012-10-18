#!/usr/bin/env python
from google.appengine.ext.webapp import template
import datastore
import json
import os
import utils
import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        context = utils.get_context()
        
        path = os.path.join(os.path.dirname(__file__), 'templates/home.html')
        self.response.out.write(template.render(path, context))

class AddVehicleHandler(webapp2.RequestHandler):
    def get(self, makeOption, model):
        context = utils.get_context()
        
        if makeOption == "addvehicle":
            context["vehicles"] = datastore.getListOfMakes()
            
            path = os.path.join(os.path.dirname(__file__), 'templates/addvehicle.html')
            self.response.out.write(template.render(path, context))
        elif not model:
            modelList = datastore.getListOfModels(makeOption)
            self.response.headerlist = [('Content-type', 'application/json')]
            self.response.out.write(json.dumps(modelList))
        else:
            yearList = datastore.getListOfYears(makeOption, model)
            self.response.headerlist = [('Content-type', 'application/json')]
            self.response.out.write(json.dumps(yearList))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/vehicle/([^/]+)?/?(.+?)?', AddVehicleHandler),
    ('/cars/raw/([^/]+)?/?(.+?)?', AddVehicleHandler)
], debug=True)
