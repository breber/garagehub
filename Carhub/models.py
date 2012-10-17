from google.appengine.ext import db


class Show(db.Model):
    title = db.StringProperty()
    poster = db.StringProperty()

class Season(db.Model):
    show = db.ReferenceProperty(Show)
    number = db.IntegerProperty()
    poster = db.StringProperty()

class Episode(db.Model):
    show = db.ReferenceProperty(Show)
    season = db.IntegerProperty()
    number = db.IntegerProperty()
    title = db.StringProperty()
    airdate = db.DateTimeProperty()
    poster = db.StringProperty()
    watched = db.BooleanProperty()
    userid = db.StringProperty()
    