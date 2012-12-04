#!/usr/bin/env python
from google.appengine.api import users
import datastore
import json
import webapp2

class ExpenseFuelHandler(webapp2.RequestHandler):
    def get(self, vehicleId, day_range):
        self.response.headerlist = [('Content-type', 'application/json')]
        
        user = users.get_current_user()
        
        if user:
            if day_range:
                results = datastore.getFuelRecords(user.user_id(), vehicleId, long(day_range))
            else:
                results = datastore.getFuelRecords(user.user_id(), vehicleId)
            
            toRet = []
            for record in results:
                obj = {}
                obj["date"] = record.date.strftime("%m/%d/%y")
                obj["lastmodified"] = record.lastmodified.ctime()
                obj["category"] = record.category
                obj["location"] = record.location
                obj["amount"] = record.amount
                obj["odometerStart"] = record.odometerStart
                obj["odometerEnd"] = record.odometerEnd
                obj["gallons"] = record.gallons
                obj["costPerGallon"] = record.costPerGallon
                obj["fuelGrade"] = record.fuelGrade
                obj["mpg"] = record.mpg
                toRet.append(obj)
            
            self.response.out.write(json.dumps(toRet))

class ExpenseCategoryHandler(webapp2.RequestHandler):
    def get(self, vehicleId, day_range):
        self.response.headerlist = [('Content-type', 'application/json')]
        
        user = users.get_current_user()
        
        if user:
            if day_range:
                baseexpenses = datastore.getBaseExpenseRecords(user.user_id(), vehicleId, long(day_range))
            else:
                baseexpenses = datastore.getBaseExpenseRecords(user.user_id(), vehicleId)
            
            toRet = {}

            for record in baseexpenses:
                category = str(record.category)
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
    ('/api/expense/fuel/([^/]+)/?(.+?)?', ExpenseFuelHandler),
    ('/api/expense/category/([^/]+)/?(.+?)?', ExpenseCategoryHandler)
])
