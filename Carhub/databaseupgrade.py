'''
Created on Dec 10, 2012

@author: breber
'''

#from google.appengine.ext import ndb
#import datastore
#import logging
#import models
#import webapp2
#
#class CategoryUpdate(webapp2.RequestHandler):
#    def get(self, update):
#        query = models.UserExpenseCategory().query()
#        userExpenseCategories = ndb.get_multi(query.fetch(keys_only=True))
#
#        for e in userExpenseCategories:
#            if not e.owner == "defaultCategory":
#                logging.warn("CategoryUpdate: UserExpense: %s" % e.category)
#                newCategory = models.ExpenseCategory()
#                newCategory.category = e.category
#                newCategory.owner = e.owner
#
#                logging.warn("CategoryUpdate: NewUserExpense: %s" % e.category)
#                if update == "update":
#                    newCategory.put()
#
#        query = models.MaintenanceCategory().query()
#        maintenanceCategories = ndb.get_multi(query.fetch(keys_only=True))
#
#        for e in maintenanceCategories:
#            if not e.owner == "defaultMaintCategory":
#                logging.warn("CategoryUpdate: Maint: %s" % e.category)
#                newCategory = models.ExpenseCategory()
#                newCategory.category = "Maintenance"
#                newCategory.subcategory = e.category
#                newCategory.owner = e.owner
#
#                logging.warn("CategoryUpdate: NewMaint: %s" % e.category)
#                if update == "update":
#                    newCategory.put()
#
#
#        datastore.getMaintenanceCategoryStrings("")
#        datastore.getExpenseCategoryStrings("")
#        self.redirect("/")
#
#class ExpenseUpdate(webapp2.RequestHandler):
#    def get(self, update):
#        query = models.BaseExpense().query()
#        expenses = ndb.get_multi(query.fetch(keys_only=True))
#
#        for e in expenses:
#            logging.warn("ExpenseUpdate: %s" % e.category)
#            if e._class_name() == "FuelRecord":
#                category = datastore.get_category_by_name(e.owner, "Fuel Up")
#            else:
#                category = datastore.get_category_by_name(e.owner, e.category)
#
#            if not category:
#                category = datastore.get_category_by_name(e.owner, "Uncategorized")
#
#            e.categoryid = category.key.id()
#
#            logging.warn("ExpenseUpdate: Found: %s" % category.category)
#            if update == "update":
#                e.put()
#
#        self.redirect("/")
#
#app = webapp2.WSGIApplication([
#    ('/database/categories/?([^/]+)?', CategoryUpdate),
#    ('/database/expenses/?([^/]+)?', ExpenseUpdate),
#], debug=True)
