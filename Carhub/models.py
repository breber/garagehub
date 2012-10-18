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
    