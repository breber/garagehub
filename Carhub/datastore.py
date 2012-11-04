'''
Created on Oct 17, 2012

@author: breber
'''
from google.appengine.ext import ndb
import models
import datetime

def getUserVehicle(vehicleId):
    """Gets the UserVehicle instance for the given ID
    
    Args: 
        vehicleId - The vehicle ID
    
    Returns
        The UserVehicle with the given ID, None otherwise
    """

    return models.UserVehicle.get_by_id(long(vehicleId))

def getFuelRecords(userId, vehicleId, day_range=30):
    """Gets the FuelRecords for the given vehicle ID
    
    Args: 
        vehicleId - The vehicle ID
        day_range - The time range
    
    Returns
        The list of FuelRecords
    """
    
    delta = datetime.timedelta(days=day_range)
    date = datetime.datetime.now() - delta
    query = models.FuelRecord().query(models.FuelRecord.owner == userId,
                                      models.FuelRecord.vehicle == long(vehicleId),
                                      models.FuelRecord.date >= date)
    query = query.order(models.FuelRecord.date)
    results = ndb.get_multi(query.fetch(keys_only=True))

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
        toRet.append(obj)
        
    return toRet

def getUserExpenseCategories(userId):
    """Gets a list of user categories (strings)
    
    Args: 
        userId - The user ID
    
    Returns
        A string list of categories for that user
    """

    query = models.UserExpenseCategory().query(models.UserExpenseCategory.owner == userId)
    results = ndb.get_multi(query.fetch(keys_only=True))

    toRet = []
    
    # TODO: declare default categories for expenses somewhere else
    # BR COMMENT: maybe just store the defaults as categories with
    #             an owner = "none" or something?
    toRet.append("Maintenance")
    toRet.append("Fuel Up")
    toRet.append("Repair")
    toRet.append("Uncategorized")
    
    for c in results:
        if not c.category in toRet:
            toRet.append(c.category)
    
    toRet.sort()
    
    return toRet


def getListOfMakes():
    """Gets a list of vehicle makes (strings)
    
    Returns
        A string list of BaseVehicle makes
    """

    query = models.BaseVehicle().query()
    results = ndb.get_multi(query.fetch(keys_only=True))

    toRet = []
    for v in results:
        if not v.make in toRet:
            toRet.append(v.make)
    
    toRet.sort()
    
    return toRet

def getListOfModels(make):
    """Gets a list of vehicle models (strings)
    
    Args: 
        make - The vehicle make to get models for
    
    Returns
        A string list of BaseVehicle models for the given make
    """

    query = models.BaseVehicle().query(models.BaseVehicle.make == make)
    results = ndb.get_multi(query.fetch(keys_only=True))

    toRet = []
    for v in results:
        if not v.model in toRet:
            toRet.append(v.model)
    
    toRet.sort()
    
    return toRet

def getListOfYears(make, model):
    """Gets a list of years for a given make and model
    
    Args: 
        make - The vehicle make
        model - The vehicle model
    
    Returns
        A string list of BaseVehicle years for the given make and model
    """

    query = models.BaseVehicle().query(models.BaseVehicle.make == make, 
                                       models.BaseVehicle.model == model)
    result = query.get()
    
    toRet = result.years.split(",")
    toRet.sort()
    
    return toRet
        