'''
Created on Oct 17, 2012

@author: breber
'''
from google.appengine.ext import ndb
import datetime
import models

def getUserVehicle(userId, vehicleId):
    """Gets the UserVehicle instance for the given ID
    
    Args: 
        vehicleId - The vehicle ID
    
    Returns
        The UserVehicle with the given ID, None otherwise
    """

    car = models.UserVehicle.get_by_id(long(vehicleId))
    
    if car and car.owner == userId:   
        return car
    else:
        return None

def getBaseExpenseRecords(userId, vehicleId, day_range=30):
    """Gets the BaseExpense for the given vehicle ID
    
    Args: 
        vehicleId - The vehicle ID
        day_range - The time range
    
    Returns
        The list of BaseExpense
    """
    
    delta = datetime.timedelta(days=day_range)
    date = datetime.datetime.now() - delta
    query = models.BaseExpense().query(models.BaseExpense.owner == userId,
                                       models.BaseExpense.vehicle == long(vehicleId),
                                       models.BaseExpense.date >= date)
    query = query.order(models.BaseExpense.date)
    return ndb.get_multi(query.fetch(keys_only=True))

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
    return ndb.get_multi(query.fetch(keys_only=True))

def getMaintenanceRecords(userId, vehicleId, day_range=30):
    """Gets the MaintenanceRecords for the given vehicle ID
    
    Args: 
        vehicleId - The vehicle ID
        day_range - The time range
    
    Returns
        The list of MaintenanceRecords
    """
    
    delta = datetime.timedelta(days=day_range)
    date = datetime.datetime.now() - delta
    query = models.MaintenanceRecord().query(models.MaintenanceRecord.owner == userId,
                                             models.MaintenanceRecord.vehicle == long(vehicleId),
                                             models.MaintenanceRecord.date >= date)
    query = query.order(models.MaintenanceRecord.date)
    return ndb.get_multi(query.fetch(keys_only=True))

def getMaintenanceCategories(userId):
    """Gets a list of user categories (strings)
    
    Args: 
        userId - The user ID
    
    Returns
        A string list of categories for that user
    """

    query = models.MaintenanceCategory().query(models.MaintenanceCategory.owner == userId)
    results = ndb.get_multi(query.fetch(keys_only=True))

    toRet = []
    
    for c in results:
        if not c.category in toRet:
            toRet.append(c.category)
    
    toRet.sort()
    
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
        