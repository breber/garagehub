#!/usr/bin/env python
from google.appengine.api import urlfetch
import json
import logging
import models
import re

def performUpdate():
    """ Wrapper for using the FetchBaseVehicles module """

    fetcher = FetchBaseVehicles()
    fetcher.updateVehicles()

class FetchBaseVehicles:
    """ Module for updating list of BaseVehicles """
    vehicleList = []
    numAdded = 0
    numUpdated = 0
    numSkipped = 0
    serverResponse = ""

    def updateVehicles(self):
        """ Perform an update of all the vehicles from Cars.com """

        url = "http://www.cars.com/js/mmyCrp.js"
        result = urlfetch.fetch(url=url, payload=None, method=urlfetch.GET, deadline=30)

        if result.status_code == 200:
            firstIndex = result.content.index("[")
            lastIndex = result.content.rindex("]") + 1
            self.serverResponse = result.content[firstIndex:lastIndex]

            # Make the JSON standards compliant (Cars.com should really fix their
            # JSON so that I don't have to do this crazy stuff)

            # replace all single quotes with double quotes
            self.serverResponse = self.serverResponse.replace("'", "\"")
            # Surround all of the first keys with quotes
            self.serverResponse = re.sub("{(.+?):", "{\"\g<1>\":", self.serverResponse)
            # Surround all of the remaining keys with quotes
            self.serverResponse = re.sub(",([^\"}]+?):", ",\"\g<1>\":", self.serverResponse)

            # Get the records that need updating
            self.getUpdatedRecords()

            # Update the records in the database
            self.updateDatabase()

            logging.info("Finished Updating")
            logging.info("Num Updated: %d" % self.numUpdated)
            logging.info("Num Added: %d" % self.numAdded)
            logging.info("Num Skipped: %d" % self.numSkipped)


    def getUpdatedRecords(self):
        """ Parse the data and figure out which BaseVehicles need to be added/updated """

        prevResult = models.ServerResponseString.query().get()
        prevJson = None
        skip = False

        # If we have previously received data, get the string
        # representation we recieved
        if prevResult:
            prevJson = json.loads(prevResult.response)

            # If what we had before matches what we just
            # received, then there is no need to updated
            if prevResult.response == self.serverResponse:
                skip = True

        # If we need to updated perform this
        if not skip:
            jsonDecoded = json.loads(self.serverResponse)

            # For each make in the list from the server
            for obj in jsonDecoded:
                # Grab relevant data
                makeObj = obj["mk"]
                modelsArr = obj["mds"]
                makeString = makeObj["n"]

                # For each model in this make
                for model in modelsArr:
                    # Grab relevant data
                    modelStr = model["dn"]
                    yearsStr = model["yrs"]

                    # Get the list of years we currently have in the database
                    prevYears = self.getYears(prevJson, makeString, modelStr)

                    # If we didn't find years, or the previous doesn't
                    # match the current, then build a new Vehicle and
                    # add it to the list of Vehicles to update in the database
                    if not prevYears or prevYears != yearsStr:
                        toAdd = models.BaseVehicle()
                        toAdd.make = makeString
                        toAdd.model = modelStr
                        toAdd.years = yearsStr

                        self.vehicleList.append(toAdd)
                    else:
                        # Just note that we skipped a vehicle
                        self.numSkipped = self.numSkipped + 1

            # Store the new response from the server into
            # the database
            toSave = None
            if prevResult:
                toSave = prevResult
            else:
                toSave = models.ServerResponseString()

            toSave.response = self.serverResponse
            toSave.put()
        else:
            self.numAdded = -1
            self.numUpdated = -1
            self.numSkipped = -1


    def getYears(self, json, make, model):
        """ Get the list of years for the given make and model from the JSON array given """
        if not json:
            return None

        for obj in json:
            makeObj = obj["mk"]
            modelsArr = obj["mds"]
            makeString = makeObj["n"]

            if makeString == make:
                for modelObj in modelsArr:
                    modelString = modelObj["dn"]

                    if modelString == model:
                        return modelObj["yrs"]

        return None


    def updateDatabase(self):
        """ Go through the previously made list of BaseVehicles and updated the database """

        # For each vehicle in the list to update
        for vehicle in self.vehicleList:
            # Create a query to get the current copy
            query = models.BaseVehicle.query(models.BaseVehicle.make == vehicle.make,
                                             models.BaseVehicle.model == vehicle.model)

            result = query.get()

            # If we have the make/model in the database,
            # indicate that we updated a record, and
            # actually update the years field
            if result:
                self.numUpdated = self.numUpdated + 1

                result.years = vehicle.years
                result.put()
            else:
                # Otherwise, add the vehicle to the database
                self.numAdded = self.numAdded + 1
                vehicle.put()

