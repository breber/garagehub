from google.appengine.ext import ndb
import utils

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

    def name(self):
        return "%s %s %s" % (self.year, self.make, self.model)

class BaseExpense(ndb.Model):
    owner = ndb.StringProperty()
    vehicle = ndb.IntegerProperty()
    date = ndb.DateProperty()
    lastmodified = ndb.DateTimeProperty()
    category = ndb.StringProperty()
    location = ndb.StringProperty()
    description = ndb.StringProperty()
    amount = ndb.FloatProperty()
    picture = ndb.StringProperty()

    def date_formatted(self):
        return utils.format_date(self.date)

    def amount_formatted(self):
        return utils.format_float(self.amount)
    
    def name(self):
        return "%s %s %s %s" % (self.date, self.location, self.category, self.amount)

class MaintenanceRecord(BaseExpense):
    odometer = ndb.IntegerProperty()
    
    def odometer_formatted(self):
        return utils.format_int(self.odometer)

class FuelRecord(BaseExpense):
    mpg = ndb.FloatProperty()
    odometerStart = ndb.IntegerProperty()
    odometerEnd = ndb.IntegerProperty()
    gallons = ndb.FloatProperty()
    costPerGallon = ndb.FloatProperty()
    fuelGrade = ndb.StringProperty()

    def mpg_formatted(self):
        return utils.format_float(self.mpg)

    def odometerStart_formatted(self):
        return utils.format_int(self.odometerStart)

    def odometerEnd_formatted(self):
        return utils.format_int(self.odometerEnd)

    def gallons_formatted(self):
        return utils.format_float(self.gallons)

    def costPerGallon_formatted(self):
        return utils.format_float(self.costPerGallon)

class UserExpenseCategory(ndb.Model):
    owner = ndb.StringProperty()
    category = ndb.StringProperty()
    
    def name(self):
        return self.category
    
class MaintenanceCategory(ndb.Model):
    owner = ndb.StringProperty()
    category = ndb.StringProperty()
    
    def name(self):
        return self.category

class Notification(ndb.Model):
    owner = ndb.StringProperty()
    vehicle = ndb.IntegerProperty()
    vehicleName = ndb.StringProperty()
    category = ndb.StringProperty()
    recurring = ndb.BooleanProperty()
    dateBased = ndb.BooleanProperty()
    mileBased = ndb.BooleanProperty()
    date = ndb.DateProperty()
    mileage = ndb.IntegerProperty()
    notifyDaysBefore = ndb.IntegerProperty()
    notifyMilesBefore = ndb.IntegerProperty()
    recurringMiles = ndb.IntegerProperty()
    recurringMonths = ndb.IntegerProperty()
    dateLastSeen = ndb.DateProperty()

    def name(self):
        return "%s %s" % (self.vehicleName, self.category)