#!/usr/bin/env python
from google.appengine.api import users
import datastore
import json
import utils
import webapp2

class UserVehicleHandler(webapp2.RequestHandler):
    def get(self, parameter1):
        self.response.headerlist = [('Content-type', 'application/json')]

        user = users.get_current_user()
        results = datastore.getUserVehicleList(user.user_id())

        self.response.out.write(json.dumps(results, cls=utils.ComplexEncoder))

class ExpenseFuelHandler(webapp2.RequestHandler):
    def get(self, vehicleId, day_range):
        self.response.headerlist = [('Content-type', 'application/json')]

        user = users.get_current_user()

        if day_range:
            results = datastore.getFuelRecords(user.user_id(), vehicleId, long(day_range))
        else:
            results = datastore.getFuelRecords(user.user_id(), vehicleId, day_range=None)
        self.response.out.write(json.dumps(results, cls=utils.ComplexEncoder))
        
class ExpenseMaintenanceHandler(webapp2.RequestHandler):
    def get(self, vehicleId, day_range):
        self.response.headerlist = [('Content-type', 'application/json')]
        
        user = users.get_current_user()
        
        if day_range:
            results = datastore.getMaintenanceRecords(user.user_id(), vehicleId, long(day_range))
        else:
            results = datastore.getMaintenanceRecords(user.user_id(), vehicleId, day_range=None)
        
        self.response.out.write(json.dumps(results, cls=utils.ComplexEncoder))

class ExpenseCategoryHandler(webapp2.RequestHandler):
    def get(self, vehicleId, day_range):
        self.response.headerlist = [('Content-type', 'application/json')]

        user = users.get_current_user()

        if day_range:
            baseexpenses = datastore.getBaseExpenseRecords(user.user_id(), vehicleId, long(day_range))
        else:
            baseexpenses = datastore.getBaseExpenseRecords(user.user_id(), vehicleId)

        toRet = {}

        for record in baseexpenses:
            category = datastore.getCategoryById(record.owner, record.categoryid).category
            prev = 0
            if category in toRet.keys():
                prev = toRet[category]
            toRet[category] = prev + record.amount

        toRet1 = []
        for cat in toRet.keys():
            category = []
            category.append(cat)
            category.append(toRet[cat])
            toRet1.append(category)

        self.response.out.write(json.dumps(toRet1))

app = webapp2.WSGIApplication([
    ('/api/vehicles/?(.+?)?', UserVehicleHandler),
    ('/api/expense/fuel/([^/]+)/?(.+?)?', ExpenseFuelHandler),
    ('/api/expense/maintenance/([^/]+)/?(.+?)?', ExpenseMaintenanceHandler),
    ('/api/expense/category/([^/]+)/?(.+?)?', ExpenseCategoryHandler)
])
