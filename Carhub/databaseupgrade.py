'''
Created on Dec 10, 2012

@author: breber
'''

from google.appengine.api import images
from google.appengine.ext import ndb
import datastore
import logging
import models
import webapp2

#class DatabaseUpgrade(webapp2.RequestHandler):
#    def get(self):
#        query = models.BaseExpense().query()
#        expenses = ndb.get_multi(query.fetch(keys_only=True))
#        
#        for e in expenses:
#            if e.picture:
#                e.pictureurl = images.get_serving_url(e.picture, 400)
#                logging.warn("%s" % e.pictureurl)
#                e.put()
#        
#        self.redirect("/")
#

class CategoryUpdate(webapp2.RequestHandler):
    def get(self):
        query = models.BaseExpense().query()
        expenses = ndb.get_multi(query.fetch(keys_only=True))
        
        for e in expenses:
            logging.warn("CategoryUpdate: %s" % e.category)
            if e._class_name() == "MaintenanceRecord":
                category = datastore.getCategoryByName(e.owner, "maintenance", e.category)
            elif e._class_name() == "FuelRecord":
                category = datastore.getCategoryByName(e.owner, "expense", "Fuel Up")
            else:
                category = datastore.getCategoryByName(e.owner, "expense", e.category)
            
            if not category:
                category = datastore.getCategoryByName(e.owner, "expense", "Uncategorized")

            e.categoryid = category.key.id()
                        
            logging.warn("CategoryUpdate: Found: %s" % category.category)
            e.put()

        self.redirect("/")

app = webapp2.WSGIApplication([ 
#    ('/database/upgrade', DatabaseUpgrade),
    ('/database/updatecategories', CategoryUpdate),
], debug=True)
