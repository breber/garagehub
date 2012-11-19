#!/usr/bin/env python
from google.appengine.api import urlfetch, users
from google.appengine.ext import ndb
import datetime
import json
import models
import webapp2

class FetchCarsBrian(webapp2.RequestHandler):
    def get(self):
        url = "http://nosec.auto-records.appspot.com/getRecords"
        result = urlfetch.fetch(url=url, payload=None, method=urlfetch.GET, deadline=30)
        
        if result.status_code == 200:
            jsonResult = json.loads(result.content)
            
            for vehicle in jsonResult:
                if vehicle["emailAddress"] == "reber.brian@gmail.com":
                    veh = models.UserVehicle()
                    veh.make = vehicle["make"]
                    veh.model = vehicle["model"]
                    veh.owner = vehicle["userId"]
                    veh.year = vehicle["year"]
                    veh.color = vehicle["color"]
                    veh.plates = vehicle["licensePlate"]
                    veh.lastmodified = datetime.datetime.now()
                    veh.put()

                    vehicleId = veh.key.id()
                    fuelRecords = vehicle["fuelRecords"]
                    prevOdometer = -1
                    for fuel in fuelRecords:
                        toAdd = models.FuelRecord()
                        toAdd.vehicle = vehicleId
                        toAdd.owner = fuel["userId"]
                        toAdd.date = datetime.datetime.fromtimestamp((fuel["date"] / 1000))
                        toAdd.lastmodified = datetime.datetime.now()
                        toAdd.category = "Fuel"
                        toAdd.location = fuel["vendor"]
                        toAdd.description = ""
                        toAdd.gallons = fuel["gallons"]
                        toAdd.costPerGallon = fuel["costPerGallon"]
                        toAdd.amount = toAdd.gallons * toAdd.costPerGallon
                        toAdd.fuelGrade = fuel["fuelGrade"]
                        toAdd.odometerStart = prevOdometer
                        prevOdometer = fuel["odometer"]
                        toAdd.odometerEnd = prevOdometer
                        toAdd.put()
                        
class UpdateFuelBrian(webapp2.RequestHandler):
    def get(self):
        query = models.FuelRecord.query(models.FuelRecord.owner == users.get_current_user().user_id())
        results = ndb.get_multi(query.fetch(keys_only=True))
        
        for f in results:
            if f.gallons != 0:
                f.mpg = (f.odometerEnd - f.odometerStart) / f.gallons
                f.category = "Fuel Record"
                f.description = "Filled up with gas"
                f.fuelGrade = "Regular"
                f.put()

app = webapp2.WSGIApplication([
    ('/brian/fetch', FetchCarsBrian),
    ('/brian/update', UpdateFuelBrian),
], debug=True)
