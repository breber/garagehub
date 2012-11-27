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
                    userId = vehicle["userId"]
                    veh = models.UserVehicle()
                    veh.make = vehicle["make"]
                    veh.model = vehicle["model"]
                    veh.owner = userId
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
                        toAdd.owner = userId
                        toAdd.date = datetime.datetime.fromtimestamp((fuel["date"] / 1000))
                        toAdd.lastmodified = datetime.datetime.now()
                        toAdd.category = "Fuel Record"
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
                        toAdd.vehicle = vehicleId
                        toAdd.owner = userId
                        toAdd.date = datetime.datetime.fromtimestamp((maint["date"] / 1000))
                        toAdd.lastmodified = datetime.datetime.now()
                        toAdd.category = "Generic Maintenance"
                        toAdd.location = maint["vendor"]
                        toAdd.description = maint["title"]
                        toAdd.amount = maint["totalCost"]
                        toAdd.odometer = maint["odometer"]
                        toAdd.put()

class DeleteRecordsBrian(webapp2.RequestHandler):
    def get(self):
        query = models.FuelRecord.query(models.FuelRecord.owner == users.get_current_user().user_id())
        results = ndb.get_multi(query.fetch(keys_only=True))
        
        for f in results:
            f.key.delete()
        
        query = models.MaintenanceRecord.query(models.MaintenanceRecord.owner == users.get_current_user().user_id())
        results = ndb.get_multi(query.fetch(keys_only=True))
        
        for m in results:
            m.key.delete()
        
        query = models.UserVehicle.query(models.UserVehicle.owner == users.get_current_user().user_id())
        results = ndb.get_multi(query.fetch(keys_only=True))
        
        for v in results:
            v.key.delete()

app = webapp2.WSGIApplication([
    ('/brian/fetch', FetchCarsBrian),
    ('/brian/delete', DeleteRecordsBrian),
], debug=True)
