#!/usr/bin/env python
from google.appengine.api import users
from google.appengine.ext.webapp import template
import datastore
import json
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

class RawVehicleHandler(webapp2.RequestHandler):
    def get(self, make, model):
        self.response.headerlist = [('Content-type', 'application/json')]
        
        if not model:
            modelList = datastore.getListOfModels(make)
            self.response.out.write(json.dumps(modelList))
        else:
            yearList = datastore.getListOfYears(make, model)
            self.response.out.write(json.dumps(yearList))
            
class NotificationHandler(webapp2.RequestHandler):
    def get(self, pageName):
        context = utils.get_context()
        user = users.get_current_user()
        
        if pageName == "add":
            path = os.path.join(os.path.dirname(__file__), 'templates/addnotification.html')
            userVehicles = datastore.getUserVehicleList(user.user_id())
            if len(userVehicles) > 0:
                context["vehicles"] = userVehicles
            userCategories = datastore.getMaintenanceCategories(user.user_id())
            if len(userCategories) > 0:
                context["categories"] = userCategories
        else:
            notifications = datastore.getNotifications(user.user_id())
            if len(notifications) > 0:
                context["notifications"] = notifications
            path = os.path.join(os.path.dirname(__file__), 'templates/notifications.html')

        self.response.out.write(template.render(path, context))
        
    def post(self):
        context = utils.get_context()
        user = users.get_current_user()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/notifications/?(.+?)?', NotificationHandler),
    ('/cars/raw/([^/]+)?/?(.+?)?', RawVehicleHandler)
], debug=True)
