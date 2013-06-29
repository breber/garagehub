#!/usr/bin/env python
from google.appengine.api import users
import datastore
import json
import models
import utils
import webapp2

class UserVehicleHandler(webapp2.RequestHandler):
    def get(self, parameter1):
        context = utils.get_context()
        self.response.headerlist = [('Content-type', 'application/json')]

        user_id = context['user']['userId']

        toRet = {}
        toRet["activeIds"] = models.UserVehicle.query(models.UserVehicle.owner == user_id).fetch(keys_only=True)
        toRet["vehicles"] = datastore.get_all_user_vehicles(user_id)

        self.response.out.write(json.dumps(toRet, cls=utils.ComplexEncoder))

class ExpenseBaseExpenseHandler(webapp2.RequestHandler):
    def get(self, vehicle_id, last_modified=0):
        context = utils.get_context()
        self.response.headerlist = [('Content-type', 'application/json')]

        if not last_modified:
            last_modified = "0"

        user_id = context['user']['userId']
        results = datastore.get_all_expense_records(user_id, vehicle_id, long(last_modified), polymorphic=False)

        toRet = {}
        toRet["activeIds"] = datastore.get_all_expense_records(user_id, vehicle_id, long(last_modified), polymorphic=False, keys_only=True)
        toRet["records"] = results

        self.response.out.write(json.dumps(toRet, cls=utils.ComplexEncoder))

class ExpenseFuelHandler(webapp2.RequestHandler):
    def get(self, vehicle_id, last_modified=0):
        context = utils.get_context()
        self.response.headerlist = [('Content-type', 'application/json')]

        if not last_modified:
            last_modified = "0"

        user_id = context['user']['userId']
        results = datastore.get_fuel_records(user_id, vehicle_id, long(last_modified))

        toRet = {}
        toRet["activeIds"] = models.FuelRecord.query(models.FuelRecord.owner == user_id).fetch(keys_only=True)
        toRet["records"] = results

        self.response.out.write(json.dumps(toRet, cls=utils.ComplexEncoder))

class ExpenseMaintenanceHandler(webapp2.RequestHandler):
    def get(self, vehicle_id, last_modified=0):
        context = utils.get_context()
        self.response.headerlist = [('Content-type', 'application/json')]

        if not last_modified:
            last_modified = "0"

        user_id = context['user']['userId']
        results = datastore.get_maintenance_records(user_id, vehicle_id, long(last_modified))

        toRet = {}
        toRet["activeIds"] = models.MaintenanceRecord.query(models.MaintenanceRecord.owner == user_id).fetch(keys_only=True)
        toRet["records"] = results

        self.response.out.write(json.dumps(toRet, cls=utils.ComplexEncoder))

class ExpenseCategoryHandler(webapp2.RequestHandler):
    def get(self, vehicle_id, last_modified=0):
        context = utils.get_context()
        self.response.headerlist = [('Content-type', 'application/json')]

        if not last_modified:
            last_modified = "0"

        user_id = context['user']['userId']
        baseexpenses = datastore.get_all_expense_records(user_id, vehicle_id, long(last_modified))

        toRet = {}

        for record in baseexpenses:
            category = datastore.get_category_by_id(record.owner, record.categoryid).category
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
