#!/usr/bin/env python
from google.appengine.api import urlfetch, users
from google.appengine.ext import ndb
import datastore
import datetime
import json
import models
import os
import utils
import webapp2

class BackupDataBrian(webapp2.RequestHandler):
    def get(self):
        context = utils.get_context()
        self.response.headerlist = [('Content-type', 'application/json')]

        user_id = context['user']['userId']

        toRet = {}
        toRet["vehicles"] = []
        vehicles = datastore.get_all_user_vehicles(user_id)
        for vehicle in vehicles:
            vehicle_id = vehicle.key.id()
            vh = {}
            vh["fuelRecords"] = datastore.get_fuel_records(user_id, vehicle_id, None)
            vh["maintenanceRecords"] = datastore.get_maintenance_records(user_id, vehicle_id, None)
            vh["expenseRecords"] = datastore.get_all_expense_records(user_id, vehicle_id, None, polymorphic=False)

            toRet["vehicles"].append(vh)

        self.response.out.write(json.dumps(toRet, cls=utils.ComplexEncoder))

app = webapp2.WSGIApplication([
    ('/brian/backup', BackupDataBrian)
], debug=True)
