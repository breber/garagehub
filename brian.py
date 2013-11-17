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

class FetchCarsBrian(webapp2.RequestHandler):
    def get(self):
        # Only run in dev environment
        if not os.environ['SERVER_SOFTWARE'].startswith('Dev'):
            self.redirect("/")
            return

        context = utils.get_context(False)
        url = self.request.url.replace("/brian/fetch", "/static/js/sampledata.json")
        result = urlfetch.fetch(url=url, payload=None, method=urlfetch.GET, deadline=30)

        if result.status_code == 200:
            jsonResult = json.loads(result.content)

            for vehicle in jsonResult:
                user_id = context['user']['userId']

                veh = models.UserVehicle()
                veh.make = vehicle["make"]
                veh.model = vehicle["model"]
                veh.owner = user_id
                veh.year = vehicle["year"]
                veh.color = vehicle["color"]
                veh.plates = vehicle["licensePlate"]
                veh.lastmodified = datetime.datetime.now()
                veh.put()

                vehicle_id = veh.key.id()
                fuelRecords = vehicle["fuelRecords"]
                prevOdometer = -1
                for fuel in fuelRecords:
                    toAdd = models.FuelRecord()
                    toAdd.vehicle = vehicle_id
                    toAdd.owner = user_id
                    toAdd.date = datetime.datetime.fromtimestamp((fuel["date"] / 1000))
                    toAdd.lastmodified = datetime.datetime.now()
                    toAdd.categoryid = datastore.get_category_by_name(user_id, "Fuel Up").key.id()
                    toAdd.location = fuel["vendor"]
                    toAdd.description = "Filled up with gas"
                    toAdd.gallons = fuel["gallons"]
                    toAdd.costPerGallon = fuel["costPerGallon"]
                    toAdd.amount = toAdd.gallons * toAdd.costPerGallon

                    fuelGrade = fuel["fuelGrade"]

                    if fuelGrade == 87:
                        toAdd.fuelGrade = "Regular"
                    elif fuelGrade == 89:
                        toAdd.fuelGrade = "Mid"
                    else:
                        toAdd.fuelGrade = "Regular"
                    toAdd.odometerStart = prevOdometer
                    prevOdometer = fuel["odometer"]
                    toAdd.odometerEnd = prevOdometer

                    if toAdd.gallons != 0 and toAdd.odometerStart > -1:
                        toAdd.mpg = (toAdd.odometerEnd - toAdd.odometerStart) / toAdd.gallons
                    else:
                        toAdd.mpg = -1

                    toAdd.put()

                maintRecords = vehicle["maintenanceRecords"]
                for maint in maintRecords:
                    toAdd = models.MaintenanceRecord()
                    toAdd.vehicle = vehicle_id
                    toAdd.owner = user_id
                    toAdd.date = datetime.datetime.fromtimestamp((maint["date"] / 1000))
                    toAdd.lastmodified = datetime.datetime.now()
                    toAdd.categoryid = datastore.get_category_by_name(user_id, "Uncategorized", True).key.id()
                    toAdd.location = maint["vendor"]
                    toAdd.description = maint["title"]
                    toAdd.amount = maint["totalCost"]
                    toAdd.odometer = maint["odometer"]
                    toAdd.put()

        self.redirect("/")

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
    ('/brian/fetch', FetchCarsBrian),
    ('/brian/backup', BackupDataBrian)
], debug=True)
