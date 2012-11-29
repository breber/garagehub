#!/usr/bin/env python
from google.appengine.api import users
from google.appengine.ext.webapp import template
import datastore
import datetime
import json
import models
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
        
    def post(self, pageName):
        context = utils.get_context()
        user = users.get_current_user()
        
        newNotificationObj = models.Notification()
        newNotificationObj.owner = user.user_id()
        vehicleId = int(self.request.get("selectVehicle", 0))
        newNotificationObj.vehicle = vehicleId
        vehicleName = datastore.getUserVehicle(user.user_id(), vehicleId)
        newNotificationObj.vehicleName = vehicleName.name()
        category = self.request.get("selectCategory", None)
        newNotificationObj.category = category
        recurring = bool(self.request.get("frequencyRadio", False))
        newNotificationObj.recurring = recurring
        dateBased = bool(self.request.get("dateCheckbox", False))
        newNotificationObj.dateBased = dateBased
        mileBased = bool(self.request.get("mileageCheckbox", False))
        newNotificationObj.mileBased = mileBased
        daysBefore = self.request.get("daysAdvance", 0)
        if daysBefore == '':
            daysBefore = 0
        newNotificationObj.notifyDaysBefore = int(daysBefore)
        milesBefore = self.request.get("milesAdvance", 0)
        if milesBefore == '':
            milesBefore = 0
        newNotificationObj.notifyMilesBefore = int(milesBefore)
        recurringMiles = self.request.get("recurrMiles", 0)
        if recurringMiles == '':
            recurringMiles = 0
        newNotificationObj.recurringMiles = int(recurringMiles)
        recurringMonths = self.request.get("recurrMonths", 0)
        if recurringMonths == '':
            recurringMonths = 0
        newNotificationObj.recurringMonths = int(recurringMonths)
        newNotificationObj.dateLastSeen = datetime.date.min
        
        if recurring:
            if dateBased:
                lastMaintRecord = datastore.getMostRecentMaintRecord(user.user_id(), vehicleId, category)
                if lastMaintRecord:
                    lastRecordedDate = lastMaintRecord.date
                else:
                    lastRecordedDate = datetime.date
                notifyYear = lastRecordedDate.year + recurringMonths / 12
                notifyMonth = lastRecordedDate.month + (recurringMonths % 12)
                if notifyMonth > 12:
                    notifyMonth -= 12
                    notifyYear += 1
                newNotificationObj.date = datetime.date(notifyYear, notifyMonth, lastRecordedDate.day)
            if mileBased:
                lastMileage = datastore.getLastRecordedMileage(user.user_id(), vehicleId)
                if not lastMileage:
                    lastMileage = 0
                newNotificationObj.mileage = lastMileage + recurringMiles
        else:
            if dateBased:
                dateString = self.request.get("dateToNotify", None)
                if dateString:
                    newNotificationObj.date = datetime.datetime.strptime(dateString, "%Y-%m-%d")
            if mileBased:
                newNotificationObj.mileage = int(self.request.get("milesToNotify", None))
                
        newNotificationObj.put()
        
        self.redirect("/notifications")
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/notifications/?(.+?)?', NotificationHandler),
    ('/cars/raw/([^/]+)?/?(.+?)?', RawVehicleHandler)
], debug=True)
