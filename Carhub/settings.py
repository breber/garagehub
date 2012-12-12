#!/usr/bin/env python
from google.appengine.api import users
from google.appengine.ext.webapp import template
import os
import utils
import webapp2
import datastore
import logging
import models

class SettingsHandler(webapp2.RequestHandler):
    def get(self, pageName, pageType, action, categoryId):
        context = utils.get_context()
        user = users.get_current_user()
        
        logging.warn("pageName = %s, pageType = %s" % (pageName, pageType))
        
        if user:
            if action == "delete":
                # Delete record
                category = datastore.getCategoryById(user.user_id(), categoryId)
                if category:
                    category.key.delete()
                else:
                    logging.warn("No category object was deleted. Couldn't find it.")
    
                self.redirect("/settings")
                return
            
            # go to regular settings page
            context["categories"] = datastore.getExpenseCategoryModels(user.user_id(), False)
            context["defaultcategories"] = datastore.getDefaultExpenseCategoryModels()
            context["maintcategories"] = datastore.getMaintenanceCategoryModels(user.user_id(), False)
            context["defaultmaintcategories"] = datastore.getDefaultMaintenanceCategoryModels()
            path = os.path.join(os.path.dirname(__file__), 'templates/settings.html')
            self.response.out.write(template.render(path, context))
       
        else:
            self.redirect("/")
    def post(self, pageName, pageType, action, categoryId):
        user = users.get_current_user()
        if user:
            if action == "add":
                if pageType == "maintenance":
                    categories = datastore.getMaintenanceCategoryStrings(user.user_id())
                else:
                    categories = datastore.getExpenseCategoryStrings(user.user_id())
                    
                newName = self.request.get("categoryName", None)
                if newName and not newName in categories:
                    # this is a new category, add it to the database
                    if pageType == "maintenance":
                        newCategoryObj = models.ExpenseCategory()
                        newCategoryObj.category = "Maintenance"
                        newCategoryObj.subcategory = newName
                    else:
                        newCategoryObj = models.ExpenseCategory()
                        newCategoryObj.category = newName
                    newCategoryObj.owner = user.user_id()
                    newCategoryObj.put()
            
            if action == "edit":
                # Edit record
                if pageType == "maintenance":
                    categories = datastore.getMaintenanceCategoryStrings(user.user_id())
                else:
                    categories = datastore.getExpenseCategoryStrings(user.user_id())
                    
                newName = self.request.get("categoryName", None)
                category = datastore.getCategoryById(user.user_id(), pageType, categoryId)
                newName = self.request.get("categoryName", None)
                logging.warn("New Name %s" % newName)
                if category and newName and not newName in categories:
                    category.category = newName
                    category.put()
                else:
                    #TODO: need a way to give user feedback about why the record was not edited
                    logging.warn("No category object was edited. Couldn't find it. Or you can't rename it to a duplicate name")
    
        self.redirect("/settings")
                
app = webapp2.WSGIApplication([
    ('/settings/?([^/]+)?/?([^/]+)?/?([^/]+)?/?(.+)?', SettingsHandler)
])

