from google.appengine.ext import db


class ServerResponseString(db.Model):
    response = db.TextProperty()

class BaseVehicle(db.Model):
    make = db.StringProperty()
    model = db.StringProperty()
    years = db.StringProperty() # StringListProperty?

class UserVehicle(db.Model):
    # TODO: last modified date?
    make = db.StringProperty()
    model = db.StringProperty()
    owner = db.StringProperty()
    year = db.StringProperty()
    color = db.StringProperty()
    plates = db.StringProperty()
    