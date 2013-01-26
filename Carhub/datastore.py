'''
Created on Oct 17, 2012

@author: breber
'''
from google.appengine.api import images
from google.appengine.ext import blobstore, ndb
import datetime
import models
import utils
import logging

def getUserVehicle(user_id, vehicle_id):
    """Gets the UserVehicle instance for the given ID

    Args:
        vehicle_id - The vehicle ID

    Returns
        The UserVehicle with the given ID, None otherwise
    """

    car = models.UserVehicle.get_by_id(long(vehicle_id))

    if car and car.owner == user_id:
        return car
    else:
        return None

def getUserVehicleList(user_id):
    """Gets a list of vehicles for the given user

    Args:
        user_id - The user ID

    Returns
        The list of user's vehicles
    """

    userVehiclesQuery = models.UserVehicle.query(models.UserVehicle.owner == user_id)
    return ndb.get_multi(userVehiclesQuery.fetch(keys_only=True))

def getAllExpenseRecords(user_id, vehicle_id, day_range=30, ascending=True):
    """Gets all the Expenses (base, maintenance, and fuel) for the given vehicle ID

    Args:
        vehicle_id - The vehicle ID
        day_range - The time range

    Returns
        The list of Expenses
    """

    return getBaseExpenseRecords(user_id, vehicle_id, day_range, ascending)

def getBaseExpenseRecords(user_id, vehicle_id, day_range=30, ascending=True, polymorphic=True):
    """Gets the BaseExpense for the given vehicle ID

    Args:
        vehicle_id - The vehicle ID
        day_range - The time range

    Returns
        The list of BaseExpense
    """

    if day_range:
        delta = datetime.timedelta(days=day_range)
        date = datetime.datetime.now() - delta
        query = models.BaseExpense().query(models.BaseExpense.owner == user_id,
                                           models.BaseExpense.vehicle == long(vehicle_id),
                                           models.BaseExpense.date >= date)
    else:
        query = models.BaseExpense().query(models.BaseExpense.owner == user_id,
                                           models.BaseExpense.vehicle == long(vehicle_id))

    if ascending:
        query = query.order(models.BaseExpense.date)
    else:
        query = query.order(-models.BaseExpense.date)
    
    if polymorphic:
        return ndb.get_multi(query.fetch(keys_only=True))
    else:
        # TODO: ideally we can get only the BaseExpenses using a query
        records = ndb.get_multi(query.fetch(keys_only=True))
        selectrecords = []
        
        for r in records:
            if r.__class__ == models.BaseExpense:
                selectrecords.append(r)
        
        return selectrecords

def getBaseExpenseRecordsIds(user_id, vehicle_id):
    """Gets the BaseExpense for the given vehicle ID

    Args:
        vehicle_id - The vehicle ID
        day_range - The time range

    Returns
        The list of BaseExpense
    """

    query = models.BaseExpense().query(models.BaseExpense.owner == user_id,
                                       models.BaseExpense.vehicle == long(vehicle_id))

    
    # TODO: ideally we can get only the BaseExpenses using a query
    records = ndb.get_multi(query.fetch(keys_only=True))
    selectrecords = []
    
    for r in records:
        if r.__class__ == models.BaseExpense:
            selectrecords.append(r.key.id())
    
    return selectrecords

def getBaseExpenseRecord(user_id, vehicle_id, expense_id):
    """Gets the BaseExpense for the given expense_id

    Args:
        vehicle_id - The vehicle ID
        expense_id - The expense ID

    Returns
        The BaseExpense
    """

    if expense_id:
        baseExpense = models.BaseExpense.get_by_id(long(expense_id))

        if baseExpense and str(baseExpense.owner) == str(user_id) and str(baseExpense.vehicle) == str(vehicle_id):
            return baseExpense

    return None

def getFuelRecords(user_id, vehicle_id, day_range=30, ascending=True):
    """Gets the FuelRecords for the given vehicle ID

    Args:
        vehicle_id - The vehicle ID
        day_range - The time range (None for all)

    Returns
        The list of FuelRecords
    """

    if day_range:
        delta = datetime.timedelta(days=day_range)
        date = datetime.datetime.now() - delta
        query = models.FuelRecord().query(models.FuelRecord.owner == user_id,
                                          models.FuelRecord.vehicle == long(vehicle_id),
                                          models.FuelRecord.date >= date)
    else:
        query = models.FuelRecord().query(models.FuelRecord.owner == user_id,
                                          models.FuelRecord.vehicle == long(vehicle_id))

    if ascending:
        query = query.order(models.FuelRecord.date)
    else:
        query = query.order(-models.FuelRecord.date)

    return ndb.get_multi(query.fetch(keys_only=True))

def getAvgGasMileage(user_id, vehicle_id):
    """Gets the Average MPG based on FuelRecords for the given vehicle ID

    Args:
        vehicle_id - The vehicle ID

    Returns
        The average mpg
    """
    fuelRecords = getFuelRecords(user_id, vehicle_id, None, False)

    milesLogged = 0
    gallonsTotal = 0
    for fuelRecord in fuelRecords:
        if fuelRecord.odometerEnd != -1 and fuelRecord.odometerStart != -1 and fuelRecord.gallons != -1:
            gallonsTotal += fuelRecord.gallons
            milesLogged += (fuelRecord.odometerEnd - fuelRecord.odometerStart)

    avgMpg = 0
    if milesLogged > 0:
        avgMpg = utils.format_float(milesLogged / gallonsTotal)

    return avgMpg

def getMilesLogged(user_id, vehicle_id):
    """Gets the miles logged based on FuelRecords for the given vehicle ID

    Args:
        vehicle_id - The vehicle ID

    Returns
        The miles logged
    """
    fuelRecords = getFuelRecords(user_id, vehicle_id, None, False)

    milesLogged = 0
    for fuelRecord in fuelRecords:
        if fuelRecord.odometerEnd != -1 and fuelRecord.odometerStart != -1:
            milesLogged += (fuelRecord.odometerEnd - fuelRecord.odometerStart)

    return utils.format_int(milesLogged)

def getCostPerMilesLogged(user_id, vehicle_id):
    """Gets the miles logged based on FuelRecords for the given vehicle ID

    Args:
        vehicle_id - The vehicle ID

    Returns
        The miles logged
    """
    fuelRecords = getFuelRecords(user_id, vehicle_id, None, False)

    milesLogged = 0
    costTotal = 0
    costPerMile = 0
    for fuelRecord in fuelRecords:
        if fuelRecord.odometerEnd != -1 and fuelRecord.odometerStart != -1:
            milesLogged += (fuelRecord.odometerEnd - fuelRecord.odometerStart)
            costTotal += (fuelRecord.gallons * fuelRecord.costPerGallon)

    if milesLogged > 0:
        costPerMile = costTotal/milesLogged

    return utils.format_float(costPerMile)

def getNFuelRecords(user_id, vehicle_id, numberToFetch=10, ascending=True):
    """Gets the FuelRecords for the given vehicle ID

    Args:
        vehicle_id - The vehicle ID
        day_range - The time range
        numberToFetch - The number of records to fetch

    Returns
        The list of FuelRecords
    """

    query = models.FuelRecord().query(models.FuelRecord.owner == user_id,
                                      models.FuelRecord.vehicle == long(vehicle_id))

    if ascending:
        query = query.order(models.FuelRecord.date)
    else:
        query = query.order(-models.FuelRecord.date)
    return ndb.get_multi(query.fetch(numberToFetch, keys_only=True))

def getMaintenanceRecords(user_id, vehicle_id, day_range=30, ascending=True):
    """Gets the MaintenanceRecords for the given vehicle ID

    Args:
        vehicle_id - The vehicle ID
        day_range - The time range

    Returns
        The list of MaintenanceRecords
    """

    if day_range:
        delta = datetime.timedelta(days=day_range)
        date = datetime.datetime.now() - delta
        query = models.MaintenanceRecord().query(models.MaintenanceRecord.owner == user_id,
                                                 models.MaintenanceRecord.vehicle == long(vehicle_id),
                                                 models.MaintenanceRecord.date >= date)
    else:
        query = models.MaintenanceRecord().query(models.MaintenanceRecord.owner == user_id,
                                                 models.MaintenanceRecord.vehicle == long(vehicle_id))

    if ascending:
        query = query.order(models.MaintenanceRecord.date)
    else:
        query = query.order(-models.MaintenanceRecord.date)

    return ndb.get_multi(query.fetch(keys_only=True))

def getMostRecentMaintRecord(user_id, vehicle_id, category):
    """Gets most recent maintenance record for category

    Args:
        user_id - The user ID
        vehicle_id - The ID of the vehicle
        category - The maintenance category being queried

    Returns
        The most recent maintenance record for specified category
    """

    query = models.MaintenanceRecord().query(models.MaintenanceRecord.owner == user_id,
                                             models.MaintenanceRecord.vehicle == vehicle_id,
                                             models.MaintenanceRecord.category == category)

    query = query.order(-models.MaintenanceRecord.date)

    maintRecord = query.get()

    return maintRecord

def getMaintenanceCategoryStrings(user_id):
    """Gets a list of user categories (strings)

    Args:
        user_id - The user ID

    Returns
        A string list of categories for that user
    """

    query = models.ExpenseCategory().query(models.ExpenseCategory.category == "Maintenance",
                                           models.ExpenseCategory.owner.IN([user_id, "defaultMaintCategory"]))
    results = ndb.get_multi(query.fetch(keys_only=True))

    if not results:
        addDefaultMaintenanceCategoryModels()

        # TODO: is this second query assignment necessary? should we be able to just refetch?
        query = models.ExpenseCategory().query(models.ExpenseCategory.category == "Maintenance",
                                               models.ExpenseCategory.owner.IN([user_id, "defaultMaintCategory"]))
        results = ndb.get_multi(query.fetch(keys_only=True))

    toRet = []

    for c in results:
        if not c.category in toRet:
            toRet.append(c.subcategory)

    toRet.sort()

    return toRet

def getMaintenanceCategoryModels(user_id, default_categories=True):
    """Gets a list of user categories (models)

    Args:
        user_id - The user ID
        default_categories - whether or not to include defaults

    Returns
        A list of categories for that user
    """
    users = [user_id]
    if default_categories:
        users.append("defaultMaintCategory")

    query = models.ExpenseCategory().query(models.ExpenseCategory.category == "Maintenance",
                                           models.ExpenseCategory.owner.IN(users))
    results = ndb.get_multi(query.fetch(keys_only=True))

    return results

def getDefaultMaintenanceCategoryModels():
    """Gets a list of user categories (models)

    Args:
        user_id - The user ID

    Returns
        A list of categories for that user
    """
    query = models.ExpenseCategory().query(models.ExpenseCategory.category == "Maintenance",
                                           models.ExpenseCategory.owner == "defaultMaintCategory")
    results = ndb.get_multi(query.fetch(keys_only=True))

    if not results:
        addDefaultMaintenanceCategoryModels()

        # TODO: is this second query assignment necessary? should we be able to just refetch?
        query = models.ExpenseCategory().query(models.ExpenseCategory.category == "Maintenance",
                                               models.ExpenseCategory.owner == "defaultMaintCategory")
        results = ndb.get_multi(query.fetch(keys_only=True))

    return results

def addDefaultMaintenanceCategoryModels():
    """Adds the default expense categories to the DB"""
    # TODO: Finalize these category defaults
    models.ExpenseCategory(owner="defaultMaintCategory", category="Maintenance", subcategory="Oil Change").put()
    models.ExpenseCategory(owner="defaultMaintCategory", category="Maintenance", subcategory="Repair").put()
    models.ExpenseCategory(owner="defaultMaintCategory", category="Maintenance", subcategory="Recall").put()
    models.ExpenseCategory(owner="defaultMaintCategory", category="Maintenance", subcategory="Uncategorized").put()


def getExpenseCategoryStrings(user_id):
    """Gets a list of user categories (strings)

    Args:
        user_id - The user ID

    Returns
        A string list of categories for that user
    """

    query = models.ExpenseCategory().query(models.ExpenseCategory.category != "Maintenance",
                                           models.ExpenseCategory.owner.IN([user_id, "defaultCategory"]))
    results = ndb.get_multi(query.fetch(keys_only=True))

    if not results:
        addDefaultExpenseCategoryModels()

        # TODO: is this second query assignment necessary? should we be able to just refetch?
        query = models.ExpenseCategory().query(models.ExpenseCategory.category != "Maintenance",
                                               models.ExpenseCategory.owner.IN([user_id, "defaultCategory"]))
        results = ndb.get_multi(query.fetch(keys_only=True))

    toRet = []
    for r in results:
        if r.subcategory:
            toRet.append(r.subcategory)
        else:
            toRet.append(r.category)

    return toRet

def getExpenseCategoryModels(user_id, default_categories=True):
    """Gets a list of user categories (models)

    Args:
        user_id - The user ID
        default_categories - whether or not to include defaults

    Returns
        A list of categories for that user
    """
    users = [user_id]

    if default_categories:
        users.append("defaultCategory")

    query = models.ExpenseCategory().query(models.ExpenseCategory.category != "Maintenance",
                                           models.ExpenseCategory.owner.IN(users))
    results = ndb.get_multi(query.fetch(keys_only=True))

    if not results and default_categories:
        addDefaultExpenseCategoryModels()

        query = models.ExpenseCategory().query(models.ExpenseCategory.category != "Maintenance",
                                               models.ExpenseCategory.owner.IN(users))
        results = ndb.get_multi(query.fetch(keys_only=True))

    return results

def getDefaultExpenseCategoryModels():
    """Gets a list of user categories (models)

    Returns
        A list of default expense categories
    """

    query = models.ExpenseCategory().query(models.ExpenseCategory.owner.IN(["defaultCategory"]))
    results = ndb.get_multi(query.fetch(keys_only=True))

    if not results:
        addDefaultExpenseCategoryModels()

        query = models.ExpenseCategory().query(models.ExpenseCategory.owner.IN(["defaultCategory"]))
        results = ndb.get_multi(query.fetch(keys_only=True))

    return results

def addDefaultExpenseCategoryModels():
    """Adds the default expense categories to the DB"""
    # If you change this be sure to change the fuel record post function to be able to find it.
    models.ExpenseCategory(owner="defaultCategory", category="Fuel Up").put()
    models.ExpenseCategory(owner="defaultCategory", category="Car Wash").put()
    models.ExpenseCategory(owner="defaultCategory", category="Uncategorized").put()

def getCategoryById(user_id, category_id):
    """Gets the BaseExpense for the given expense_id

    Args:
        vehicle_id - The vehicle ID
        expense_id - The expense ID

    Returns
        The BaseExpense
    """

    if category_id:
        expenseCategory = models.ExpenseCategory.get_by_id(long(category_id))

        if expenseCategory:
            return expenseCategory

    return None

def getCategoryByName(user_id, categoryName, maintenance_only=False):
    """Gets the BaseExpense for the given expense_id

    Args:
        vehicle_id - The vehicle ID
        expense_id - The expense ID

    Returns
        The BaseExpense
    """
    if maintenance_only:
        query = models.ExpenseCategory().query(models.ExpenseCategory.category == "Maintenance",
                                               models.ExpenseCategory.subcategory == categoryName,
                                               models.ExpenseCategory.owner.IN([user_id, "defaultMaintCategory"]))
    else:
        query = models.ExpenseCategory().query(ndb.AND(models.ExpenseCategory.owner.IN([user_id, "defaultCategory", "defaultMaintCategory"]),
                                                       ndb.OR(models.ExpenseCategory.category == categoryName,
                                                              models.ExpenseCategory.subcategory == categoryName)))

    category = query.get()
    return category


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

def getNotification(user_id, vehicle_id, category, notification_id):
    """Gets the Notification for the given notification_id

    Args:
        user_id - The user ID
        vehicle_id - The vehicle ID
        notification_id - The unique notification ID

    Returns
        The Notification
    """

    if notification_id:
        notification = models.Notification.get_by_id(long(notification_id))

        if notification and str(notification.owner) == str(user_id):
            return notification

    elif vehicle_id and category:
        query = models.Notification().query(models.Notification.owner == user_id,
                                            models.Notification.vehicle == vehicle_id,
                                            models.Notification.category == category)
        notification = query.get()

        return notification

def getNotifications(user_id):
    """Gets a list of user's notifications

    Args:
        user_id - The user ID

    Returns
        A list of user's notifications
    """

    query = models.Notification().query(models.Notification.owner == user_id)
    results = ndb.get_multi(query.fetch(keys_only=True))

    sorted(results, key=lambda Notification:Notification.name())

    return results

def getActiveDateNotifications(user_id):
    """Gets a list of date notifications to display to user

    Args:
        user_id - The user's ID

    Returns
        A list of date notifications to display
    """

    results = getNotifications(user_id)

    toRet = []

    for r in results:
        if r.dateBased:
            daysNotice = datetime.timedelta(days=r.notifyDaysBefore)
            deltaRemaining = datetime.datetime.combine(r.date, datetime.time()) - datetime.datetime.now()
            if deltaRemaining <= daysNotice:
                toRet.append(r)

    return toRet

def getActiveMileageNotifications(user_id):
    """Gets a list of mileage notifications to display to user

    Args:
        user_id - The user's ID

    Returns
        A list of mileage notifications to display
    """

    results = getNotifications(user_id)

    toRet = []

    for r in results:
        if r.mileBased:
            maxmileage = getLastRecordedMileage(user_id, r.vehicle)
            if (r.mileage - maxmileage) <= r.notifyMilesBefore:
                toRet.append(r)

    return toRet

def getLastRecordedMileage(user_id, vehicle_id):
    """Gets the user's last recorded mileage for specified vehicle

    Args:
        user_id - The user's ID
        vehicle_id - The vehicle's mileage we are querying

    Returns
        The last recorded mileage
    """

    lastMaintMileage = 0
    lastFuelMileage = 0

    maintRecordQuery = models.MaintenanceRecord().query(models.MaintenanceRecord.owner == user_id,
                                                        models.MaintenanceRecord.vehicle == vehicle_id)
    maintRecordQuery = maintRecordQuery.order(-models.MaintenanceRecord.odometer)
    lastMaintRecord = maintRecordQuery.get()
    if lastMaintRecord:
        lastMaintMileage = lastMaintRecord.odometer

    mileageQuery = models.FuelRecord().query(models.FuelRecord.owner == user_id,
                                             models.FuelRecord.vehicle == vehicle_id)
    mileageQuery = mileageQuery.order(-models.FuelRecord.odometerEnd)
    lastFuelRecord = mileageQuery.get()
    if lastFuelRecord:
        lastFuelMileage = lastFuelRecord.odometerEnd

    maxmileage = lastMaintMileage
    if lastFuelMileage > lastMaintMileage:
        maxmileage = lastFuelMileage

    return maxmileage

def getTotalCost(user_id, vehicle_id):
    """Gets the total spent on the specified vehicle

    Args:
        user_id - The user's ID
        vehicle_id - The vehicle's mileage we are querying

    Returns
        The total spent on the specified vehicle
    """

    totalCost = 0

    baseExpenses = getBaseExpenseRecords(user_id, vehicle_id, None)

    for b in baseExpenses:
        totalCost += b.amount

    return totalCost

def deleteBaseExpense(user_id, expense):
    """Deletes a BaseExpense

    Args:
        user_id - The user's ID
        expense - The expense to delete
    """
    if expense and expense.owner == user_id:
        image = expense.picture
        if image:
            images.delete_serving_url(image)
            blobstore.BlobInfo.get(image).delete()

        expense.key.delete()

def deleteUserVehicle(user_id, vehicle_id):
    """Deletes a UserVehicle, along with any related records

    Args:
        user_id - The user's ID
        vehicle_id - The vehicle to delete
    """
    vehicle = getUserVehicle(user_id, vehicle_id)
    if vehicle:
        expenseRecords = getAllExpenseRecords(user_id, vehicle_id, None)
        for r in expenseRecords:
            deleteBaseExpense(user_id, r)

        # TODO: delete notifications

        vehicle.key.delete()
