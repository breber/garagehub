from google.appengine.ext import db


class ServerResponseString(db.Model):
    response = db.TextProperty()

class BaseVehicle(db.Model):
    make = db.StringProperty()
    model = db.StringProperty()
    years = db.StringProperty() # StringListProperty?

class UserVehicle(db.Model):
    baseVehicle = db.ReferenceProperty(BaseVehicle)
    owner = db.StringProperty()
    year = db.StringProperty()
    color = db.StringProperty()
    plates = db.StringProperty()
    