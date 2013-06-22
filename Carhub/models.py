from google.appengine.ext import endpoints, ndb
from google.appengine.ext.ndb import polymodel

from protorpc import remote, messages
from endpoints_proto_datastore.ndb import EndpointsModel, EndpointsAliasProperty

import utils

class User(ndb.Model):
    email_address = ndb.StringProperty()
    is_admin = ndb.BooleanProperty(default=False)
    google_openid = ndb.StringProperty()
    google_oauth = ndb.StringProperty()

class ServerResponseString(ndb.Model):
    response = ndb.TextProperty()

class BaseVehicle(ndb.Model):
    make = ndb.StringProperty()
    model = ndb.StringProperty()
    years = ndb.StringProperty()

class UserVehicle(EndpointsModel):
    make = ndb.StringProperty()
    model = ndb.StringProperty()
    owner = ndb.StringProperty()
    year = ndb.StringProperty()
    color = ndb.StringProperty()
    plates = ndb.StringProperty()
    lastmodified = ndb.DateTimeProperty()

    @EndpointsAliasProperty(property_type=messages.StringField)
    def appengine_id(self):
        return str(self.key.id())

    def name(self):
        return "%s %s %s" % (self.year, self.make, self.model)

class ExpenseCategory(ndb.Model):
    owner = ndb.StringProperty()
    category = ndb.StringProperty()
    subcategory = ndb.StringProperty()

    def name(self):
        if self.subcategory:
            return self.subcategory

        return self.category

class BaseExpense(polymodel.PolyModel):
    owner = ndb.StringProperty()
    vehicle = ndb.IntegerProperty()
    date = ndb.DateProperty()
    lastmodified = ndb.DateTimeProperty()
    category = ndb.StringProperty() # TODO: remove this field
    categoryid = ndb.IntegerProperty()
    location = ndb.StringProperty()
    description = ndb.StringProperty()
    amount = ndb.FloatProperty()
    picture = ndb.StringProperty()
    pictureurl = ndb.StringProperty()

    def date_formatted(self):
        return utils.format_date(self.date)

    def amount_formatted(self):
        return utils.format_float(self.amount)

    def name(self):
        return "%s %s %s %s" % (self.date, self.location, self.category, self.amount)

class MaintenanceRecord(BaseExpense):
    odometer = ndb.IntegerProperty()

    def odometer_formatted(self):
        if utils.format_int(self.odometer) == "-1":
            return ""
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
