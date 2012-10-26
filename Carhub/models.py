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
    
    def name(self):
        return "%s %s %s" % (self.year, self.make, self.model)
    
class UserExpense(ndb.Model):
    owner = ndb.StringProperty()
    vehicle = ndb.StringProperty()
    purchaseDate = ndb.DateProperty()
    category = ndb.StringProperty()
    location = ndb.StringProperty()
    description = ndb.StringProperty()
    amount = ndb.StringProperty()
    lastmodified = ndb.DateTimeProperty()
    
    def name(self):
        return "%s %s %s %s" % (self.purchaseDate, self.location, self.category, self.amount)
    
class UserExpenseCategory(ndb.Model):
    owner = ndb.StringProperty()
    category = ndb.StringProperty()
    
    def name(self):
        return self.category
    