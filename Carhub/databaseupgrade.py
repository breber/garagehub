'''
Created on Dec 10, 2012

@author: breber
'''

from google.appengine.ext import ndb
import datastore
import logging
import models
import webapp2

class CategoryUpdate(webapp2.RequestHandler):
    def get(self, update):
        query = models.UserExpenseCategory().query()
        userExpenseCategories = ndb.get_multi(query.fetch(keys_only=True))
        
        for e in userExpenseCategories:
            if not e.owner == "defaultCategory":
                logging.warn("CategoryUpdate: UserExpense: %s" % e.category)
            
                        
                if update == "update":
                    e.put()

        query = models.MaintenanceCategory().query()
        maintenanceCategories = ndb.get_multi(query.fetch(keys_only=True))
        
        for e in maintenanceCategories:
            if not e.owner == "defaultMaintCategory":
                logging.warn("CategoryUpdate: Maint: %s" % e.category)
                
                        
                if update == "update":
                    e.put()

        self.redirect("/")

class ExpenseUpdate(webapp2.RequestHandler):
    def get(self, update):
        query = models.BaseExpense().query()
        expenses = ndb.get_multi(query.fetch(keys_only=True))
        
        for e in expenses:
            logging.warn("ExpenseUpdate: %s" % e.category)
            if e._class_name() == "MaintenanceRecord":
                category = datastore.getCategoryByName(e.owner, "maintenance", e.category)
            elif e._class_name() == "FuelRecord":
                category = datastore.getCategoryByName(e.owner, "expense", "Fuel Up")
            else:
                category = datastore.getCategoryByName(e.owner, "expense", e.category)
            
            if not category:
                category = datastore.getCategoryByName(e.owner, "expense", "Uncategorized")

            e.categoryid = category.key.id()
                        
            logging.warn("ExpenseUpdate: Found: %s" % category.category)
            if update == "update":
                e.put()

        self.redirect("/")

app = webapp2.WSGIApplication([ 
    ('/database/categories/?([^/]+)?', CategoryUpdate),
    ('/database/expenses/?([^/]+)?', ExpenseUpdate),
], debug=True)
