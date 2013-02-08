#!/usr/bin/env python
from google.appengine.api import users
from google.appengine.ext.webapp import template
import datetime
import datastore
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

        if not make:
            modelList = datastore.get_makes()
            self.response.out.write(json.dumps(modelList))
        elif not model:
            modelList = datastore.get_models(make)
            self.response.out.write(json.dumps(modelList))
        else:
            yearList = datastore.get_years(make, model)
            self.response.out.write(json.dumps(yearList))

class NotificationHandler(webapp2.RequestHandler):
    def get(self, page_name, notification_id):
        context = utils.get_context()
        user = users.get_current_user()

        if page_name == "add":
            path = os.path.join(os.path.dirname(__file__), 'templates/addnotification.html')
            userVehicles = datastore.get_all_user_vehicles(user.user_id())
            if len(userVehicles) > 0:
                context["vehicles"] = userVehicles
            userCategories = datastore.get_maintenance_categories(user.user_id(), as_strings=True)
            if len(userCategories) > 0:
                context["categories"] = userCategories
        else:
            if page_name == "clear":
                dateNotifications = datastore.get_active_date_notifications(user.user_id())
                for dn in dateNotifications:
                    dn.dateLastSeen = datetime.date.today()
                    dn.put()
                mileNotifications = datastore.get_active_mileage_notifications(user.user_id())
                for mn in mileNotifications:
                    mn.dateLastSeen = datetime.date.today()
                    mn.put()
            elif page_name == "delete":
                notifToDelete = models.Notification.get_by_id(long(notification_id))
                notifToDelete.key.delete()
            notifications = datastore.get_notifications(user.user_id())
            if len(notifications) > 0:
                context["notifications"] = notifications
            path = os.path.join(os.path.dirname(__file__), 'templates/notifications.html')

        self.response.out.write(template.render(path, context))

    def post(self, page_name, notification_id):
        user = users.get_current_user()
        category = self.request.get("selectCategory", None)
        vehicle_id = int(self.request.get("selectVehicle", 0))

        newNotificationObj = datastore.get_notification(user.user_id(), vehicle_id, category, None)
        if newNotificationObj:
            newNotificationObj.key.delete()

        newNotificationObj = models.Notification()
        newNotificationObj.owner = user.user_id()
        newNotificationObj.vehicle = vehicle_id
        vehicleName = datastore.get_user_vehicle(user.user_id(), vehicle_id)
        newNotificationObj.vehicleName = vehicleName.name()
        newNotificationObj.category = category
        recurring = self.request.get("frequencyRadio", False)
        newRecurring = False
        if recurring == 'False':
            newNotificationObj.recurring = False
        else:
            newNotificationObj.recurring = True
            newRecurring = True
        dateBased = self.request.get("dateCheckbox", False)
        newDateBased = False
        if dateBased:
            if dateBased == 'False':
                newNotificationObj.dateBased = False
            else:
                newNotificationObj.dateBased = True
                newDateBased = True
        mileBased = self.request.get("mileageCheckbox", False)
        newMileBased = False
        if mileBased:
            if mileBased == 'False':
                newNotificationObj.mileBased = False
            else:
                newNotificationObj.mileBased = True
                newMileBased = True
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
        else:
            recurringMiles = int(recurringMiles)
        newNotificationObj.recurringMiles = recurringMiles
        recurringMonths = self.request.get("recurrMonths", 0)
        if recurringMonths == '':
            recurringMonths = 0
        else:
            recurringMonths = int(recurringMonths)
        newNotificationObj.recurringMonths = recurringMonths

        deltaoneday = datetime.timedelta(days=1)
        newNotificationObj.dateLastSeen = datetime.date.today() - deltaoneday

        if newRecurring:
            lastMaintRecord = datastore.get_n_maint_records(user.user_id(), vehicle_id, category, 1)
            if newDateBased:
                if lastMaintRecord:
                    lastRecordedDate = lastMaintRecord.date
                else:
                    lastRecordedDate = datetime.date.today()
                yearDecimalNum = lastRecordedDate.strftime("%Y")
                monthDecimalNum = lastRecordedDate.strftime("%m")
                notifyYear = int(yearDecimalNum) + recurringMonths / 12
                notifyMonth = int(monthDecimalNum) + (recurringMonths % 12)
                if notifyMonth > 12:
                    notifyMonth -= 12
                    notifyYear += 1
                newNotificationObj.date = datetime.date(notifyYear, notifyMonth, lastRecordedDate.day)
            if newMileBased:
                lastMileage = 0
                if lastMaintRecord:
                    lastMileage = lastMaintRecord.odometer
                newNotificationObj.mileage = lastMileage + recurringMiles
        else:
            if newDateBased:
                dateString = self.request.get("dateToNotify", None)
                if dateString:
                    newNotificationObj.date = datetime.datetime.strptime(dateString, "%Y-%m-%d")
            if newMileBased:
                newNotificationObj.mileage = int(self.request.get("milesToNotify", 0))

        newNotificationObj.put()

        self.redirect("/notifications")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/notifications/?([^/]+)?/?(.+?)?', NotificationHandler),
    ('/cars/raw/?([^/]+)?/?(.+?)?', RawVehicleHandler)
], debug=True)
