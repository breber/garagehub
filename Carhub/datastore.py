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
        
def getUserVehicleList(userId):
    """Gets a list of vehicles for the given user
    
    Args: 
        userId - The user ID
    
    Returns
        The list of user's vehicles
    """
    
    userVehiclesQuery = models.UserVehicle.query(models.UserVehicle.owner == userId)
    return ndb.get_multi(userVehiclesQuery.fetch(keys_only=True))

def getAllExpenseRecords(userId, vehicleId, day_range=30, ascending=True):
    """Gets all the Expenses (base, maintenance, and fuel) for the given vehicle ID
    
    Args: 
        vehicleId - The vehicle ID
        day_range - The time range
    
    Returns
        The list of Expenses
    """
    
    return getBaseExpenseRecords(userId, vehicleId, day_range, ascending)

def getBaseExpenseRecords(userId, vehicleId, day_range=30, ascending=True):
    """Gets the BaseExpense for the given vehicle ID
    
    Args: 
        vehicleId - The vehicle ID
        day_range - The time range
    
    Returns
        The list of BaseExpense
    """
    
    if day_range:
        delta = datetime.timedelta(days=day_range)
        date = datetime.datetime.now() - delta
        query = models.BaseExpense().query(models.BaseExpense.owner == userId,
                                           models.BaseExpense.vehicle == long(vehicleId),
                                           models.BaseExpense.date >= date)
    else:
        query = models.BaseExpense().query(models.BaseExpense.owner == userId,
                                           models.BaseExpense.vehicle == long(vehicleId))
    
    if ascending:
        query = query.order(models.BaseExpense.date)
    else:
        query = query.order(-models.BaseExpense.date)
    return ndb.get_multi(query.fetch(keys_only=True))

def getBaseExpenseRecord(userId, vehicleId, expenseId):
    """Gets the BaseExpense for the given expenseId
    
    Args: 
        vehicleId - The vehicle ID
        expenseId - The expense ID
    
    Returns
        The BaseExpense
    """
    
    if expenseId:
        baseExpense = models.BaseExpense.get_by_id(long(expenseId))
        
        if baseExpense and str(baseExpense.owner) == str(userId) and str(baseExpense.vehicle) == str(vehicleId):
            return baseExpense
                                               
    return None

def getFuelRecords(userId, vehicleId, day_range=30, ascending=True):
    """Gets the FuelRecords for the given vehicle ID
    
    Args: 
        vehicleId - The vehicle ID
        day_range - The time range (None for all)
    
    Returns
        The list of FuelRecords
    """
    
    if day_range:
        delta = datetime.timedelta(days=day_range)
        date = datetime.datetime.now() - delta
        query = models.FuelRecord().query(models.FuelRecord.owner == userId,
                                          models.FuelRecord.vehicle == long(vehicleId),
                                          models.FuelRecord.date >= date)
    else:
        query = models.FuelRecord().query(models.FuelRecord.owner == userId,
                                          models.FuelRecord.vehicle == long(vehicleId))

    if ascending:
        query = query.order(models.FuelRecord.date)
    else:
        query = query.order(-models.FuelRecord.date)

    return ndb.get_multi(query.fetch(keys_only=True))

def getNFuelRecords(userId, vehicleId, numberToFetch=10, ascending=True):
    """Gets the FuelRecords for the given vehicle ID
    
    Args: 
        vehicleId - The vehicle ID
        day_range - The time range
        numberToFetch - The number of records to fetch
    
    Returns
        The list of FuelRecords
    """
    
    query = models.FuelRecord().query(models.FuelRecord.owner == userId,
                                      models.FuelRecord.vehicle == long(vehicleId))
    
    if ascending:
        query = query.order(models.FuelRecord.date)
    else:
        query = query.order(-models.FuelRecord.date)
    return ndb.get_multi(query.fetch(numberToFetch, keys_only=True))

def getMaintenanceRecords(userId, vehicleId, day_range=30, ascending=True):
    """Gets the MaintenanceRecords for the given vehicle ID
    
    Args: 
        vehicleId - The vehicle ID
        day_range - The time range
    
    Returns
        The list of MaintenanceRecords
    """
    
    if day_range:
        delta = datetime.timedelta(days=day_range)
        date = datetime.datetime.now() - delta
        query = models.MaintenanceRecord().query(models.MaintenanceRecord.owner == userId,
                                                 models.MaintenanceRecord.vehicle == long(vehicleId),
                                                 models.MaintenanceRecord.date >= date)
    else:
        query = models.MaintenanceRecord().query(models.MaintenanceRecord.owner == userId,
                                                 models.MaintenanceRecord.vehicle == long(vehicleId))
    
    if ascending:
        query = query.order(models.MaintenanceRecord.date)
    else:
        query = query.order(-models.MaintenanceRecord.date)
    
    return ndb.get_multi(query.fetch(keys_only=True))

def getMostRecentMaintRecord(userId, vehicleId, category):
    """Gets most recent maintenance record for category
    
    Args: 
        userId - The user ID
        vehicleId - The ID of the vehicle
        category - The maintenance category being queried
    
    Returns
        The most recent maintenance record for specified category
    """
    
    query = models.MaintenanceRecord().query(models.MaintenanceRecord.owner == userId,
                                             models.MaintenanceRecord.vehicle == vehicleId,
                                             models.MaintenanceRecord.category == category)
    
    query = query.order(-models.MaintenanceRecord.date)
    
    maintRecord = query.get()
    
    return maintRecord 

def getMaintenanceCategories(userId):
    """Gets a list of user categories (strings)
    
    Args: 
        userId - The user ID
    
    Returns
        A string list of categories for that user
    """

    query = models.MaintenanceCategory().query(models.MaintenanceCategory.owner.IN([userId, "defaultMaintCategory"]))
    results = ndb.get_multi(query.fetch(keys_only=True))

    if not results:
        models.MaintenanceCategory(owner="defaultMaintCategory",
                                   category="Oil Change").put()
        
        models.MaintenanceCategory(owner="defaultMaintCategory",
                                   category="Repair").put()
        
        models.MaintenanceCategory(owner="defaultMaintCategory",
                                   category="Recall").put()

        models.MaintenanceCategory(owner="defaultMaintCategory",
                                   category="Car Wash").put()
        
        query = models.MaintenanceCategory().query(models.MaintenanceCategory.owner.IN([userId, "defaultMaintCategory"]))
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

    query = models.UserExpenseCategory().query(models.UserExpenseCategory.owner.IN([userId, "defaultCategory"]))
    results = ndb.get_multi(query.fetch(keys_only=True))

    if not results:
        # TODO: some of these seem duplicated with maintenance categories...
        models.UserExpenseCategory(owner="defaultCategory",
                                   category="Maintenance").put()
        
        models.UserExpenseCategory(owner="defaultCategory",
                                   category="Fuel Up").put()
        
        models.UserExpenseCategory(owner="defaultCategory",
                                   category="Repair").put()

        models.UserExpenseCategory(owner="defaultCategory",
                                   category="Uncategorized").put()
        
        query = models.UserExpenseCategory().query(models.UserExpenseCategory.owner.IN([userId, "defaultCategory"]))
        results = ndb.get_multi(query.fetch(keys_only=True))

    toRet = []
    
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
    
def getNotifications(userId):
    """Gets a list of user's notifications
    
    Args:
        userId - The user ID
    
    Returns
        A list of user's notifications
    """

    query = models.Notification().query(models.Notification.owner == userId)
    results = ndb.get_multi(query.fetch(keys_only=True))
    
    sorted(results, key=lambda Notification:Notification.name())
    
    return results

def getActiveDateNotifications(userId):
    """Gets a list of date notifications to display to user
    
    Args:
        userId - The user's ID
    
    Returns
        A list of date notifications to display
    """
    
    results = getNotifications(userId)
    
    toRet = []
    
    for r in results:
        if r.dateLastSeen != datetime.date.today():
            if r.dateBased:
                daysNotice = datetime.timedelta(days=r.notifyDaysBefore)
                deltaRemaining = datetime.datetime.combine(r.date, datetime.time()) - datetime.datetime.now()
                if deltaRemaining <= daysNotice:
                    toRet.append(r)
                
    return toRet

def getActiveMileageNotifications(userId):
    """Gets a list of mileage notifications to display to user
    
    Args:
        userId - The user's ID
    
    Returns
        A list of mileage notifications to display
    """
    
    results = getNotifications(userId)
    
    toRet = []
    
    for r in results:
        if r.dateLastSeen != datetime.date.today():
            if r.mileBased:
                maxmileage = getLastRecordedMileage(userId, r.vehicle)
                if (r.mileage - maxmileage) <= r.notifyMilesBefore:
                    toRet.append(r)
                
    return toRet

def getLastRecordedMileage(userId, vehicleId):
    """Gets the user's last recorded mileage for specified vehicle
    
    Args:
        userId - The user's ID
        vehicleId - The vehicle's mileage we are querying
    
    Returns
        The last recorded mileage
    """
    
    lastMaintMileage = 0
    lastFuelMileage = 0

    maintRecordQuery = models.MaintenanceRecord().query(models.MaintenanceRecord.owner == userId, 
                                                        models.MaintenanceRecord.vehicle == vehicleId)
    maintRecordQuery = maintRecordQuery.order(-models.MaintenanceRecord.odometer)
    lastMaintRecord = maintRecordQuery.get()
    if lastMaintRecord:
        lastMaintMileage = lastMaintRecord.odometer
    
    mileageQuery = models.FuelRecord().query(models.FuelRecord.owner == userId,
                                             models.FuelRecord.vehicle == vehicleId)
    mileageQuery = mileageQuery.order(-models.FuelRecord.odometerEnd)
    lastFuelRecord = mileageQuery.get()
    if lastFuelRecord:
        lastFuelMileage = lastFuelRecord.odometerEnd
    
    maxmileage = lastMaintMileage
    if lastFuelMileage > lastMaintMileage:
        maxmileage = lastFuelMileage
                
    return maxmileage

def getTotalCost(userId, vehicleId):
    """Gets the total spent on the specified vehicle
    
    Args:
        userId - The user's ID
        vehicleId - The vehicle's mileage we are querying
    
    Returns
        The total spent on the specified vehicle
    """

    totalCost = 0

    baseExpenses = getBaseExpenseRecords(userId, vehicleId, None)

    for b in baseExpenses:
        totalCost += b.amount
                
    return totalCost

def deleteUserVehicle(userId, vehicleId):
    """Deletes a UserVehicle, along with any related records
    
    Args:
        userId - The user's ID
        vehicleId - The vehicle to delete
    """
    vehicle = getUserVehicle(userId, vehicleId)
    if vehicle:
        expenseRecords = getAllExpenseRecords(userId, vehicleId, None)
        for r in expenseRecords:
            r.key.delete()

        # TODO: delete notifications
        
        vehicle.key.delete()
