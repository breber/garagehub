from google.appengine.ext import ndb

class ServerResponseString(ndb.Model):
    response = ndb.TextProperty()

class BaseVehicle(ndb.Model):
    make = ndb.StringProperty()
    model = ndb.StringProperty()
    years = ndb.StringProperty()

class UserVehicle(ndb.Model):
    make = ndb.StringProperty()
    model = ndb.StringProperty()
    owner = ndb.StringProperty()
    year = ndb.StringProperty()
    color = ndb.StringProperty()
    plates = ndb.StringProperty()
    lastmodified = ndb.DateTimeProperty()

class BaseExpense(ndb.Model):
    owner = ndb.StringProperty()
    vehicle = ndb.StringProperty()
    date = ndb.DateProperty()
    lastmodified = ndb.DateTimeProperty()
    category = ndb.KeyProperty()
    location = ndb.StringProperty()
    description = ndb.StringProperty()
    amount = ndb.FloatProperty()
    picture = ndb.BlobKeyProperty()

class MaintenanceRecord(BaseExpense):
    odometer = ndb.IntegerProperty()

class FuelRecord(BaseExpense):
    odometerStart = ndb.IntegerProperty()
    odometerEnd = ndb.IntegerProperty()
    gallons = ndb.FloatProperty()
    costPerGallon = ndb.FloatProperty()
    fuelGrade = ndb.IntegerProperty()

class UserExpenseCategory(ndb.Model):
    owner = ndb.StringProperty()
    category = ndb.StringProperty()

class Notification(ndb.Model):
    owner = ndb.StringProperty()
    vehicle = ndb.StringProperty()
    # TODO
