#!/usr/bin/env python
from google.appengine.api import users
import datastore
import json
import models
import utils
import webapp2

class UserVehicleHandler(webapp2.RequestHandler):
    def get(self, parameter1):
        self.response.headerlist = [('Content-type', 'application/json')]

        user = users.get_current_user()
            
        toRet = {}
        toRet["activeIds"] = models.UserVehicle.query(models.UserVehicle.owner == user.user_id()).fetch(keys_only=True)
        toRet["vehicles"] = datastore.getUserVehicleList(user.user_id())

        self.response.out.write(json.dumps(toRet, cls=utils.ComplexEncoder))

class ExpenseBaseExpenseHandler(webapp2.RequestHandler):
    def get(self, vehicle_id, last_modified=0):
        self.response.headerlist = [('Content-type', 'application/json')]

        user = users.get_current_user()
        results = datastore.getBaseExpenseRecords(user.user_id(), vehicle_id, long(last_modified), polymorphic=False)
            
        toRet = {}
        toRet["activeIds"] = datastore.getBaseExpenseRecordsIds(user.user_id(), vehicle_id)
        toRet["records"] = results
            
        self.response.out.write(json.dumps(toRet, cls=utils.ComplexEncoder))

class ExpenseFuelHandler(webapp2.RequestHandler):
    def get(self, vehicle_id, last_modified=0):
        self.response.headerlist = [('Content-type', 'application/json')]

        user = users.get_current_user()
        results = datastore.getFuelRecords(user.user_id(), vehicle_id, long(last_modified))

        toRet = {}
        toRet["activeIds"] = models.FuelRecord.query(models.FuelRecord.owner == user.user_id()).fetch(keys_only=True)
        toRet["records"] = results

        self.response.out.write(json.dumps(toRet, cls=utils.ComplexEncoder))
        
class ExpenseMaintenanceHandler(webapp2.RequestHandler):
    def get(self, vehicle_id, last_modified=0):
        self.response.headerlist = [('Content-type', 'application/json')]
        
        user = users.get_current_user()
        results = datastore.getMaintenanceRecords(user.user_id(), vehicle_id, long(last_modified))

        toRet = {}
        toRet["activeIds"] = models.MaintenanceRecord.query(models.MaintenanceRecord.owner == user.user_id()).fetch(keys_only=True)
        toRet["records"] = results

        self.response.out.write(json.dumps(toRet, cls=utils.ComplexEncoder))

class ExpenseCategoryHandler(webapp2.RequestHandler):
    def get(self, vehicle_id, last_modified=0):
        self.response.headerlist = [('Content-type', 'application/json')]

        user = users.get_current_user()
        baseexpenses = datastore.getBaseExpenseRecords(user.user_id(), vehicle_id, long(last_modified))
        
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
    ('/api/expense/base/([^/]+)/?(.+?)?', ExpenseBaseExpenseHandler),
    ('/api/expense/fuel/([^/]+)/?(.+?)?', ExpenseFuelHandler),
    ('/api/expense/maintenance/([^/]+)/?(.+?)?', ExpenseMaintenanceHandler),
    ('/api/expense/category/([^/]+)/?(.+?)?', ExpenseCategoryHandler)
])
