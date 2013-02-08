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
    def get(self, page_name, page_type, action, category_id):
        context = utils.get_context()
        user = users.get_current_user()

        if action == "delete":
            # Delete record
            category = datastore.get_category_by_id(user.user_id(), category_id)
            if category:
                category.key.delete()
            else:
                logging.warn("No category object was deleted. Couldn't find it.")

            self.redirect("/settings")
            return

        # go to regular settings page
        context["categories"] = datastore.get_expense_categories(user.user_id(), default_categories=False)
        context["defaultcategories"] = datastore.get_expense_categories(user.user_id(), user_categories=False)
        context["maintcategories"] = datastore.get_maintenance_categories(user.user_id(), default_categories=False)
        context["defaultmaintcategories"] = datastore.get_maintenance_categories(user.user_id(), user_categories=False)

        path = os.path.join(os.path.dirname(__file__), 'templates/settings.html')
        self.response.out.write(template.render(path, context))

    def post(self, page_name, page_type, action, category_id):
        user = users.get_current_user()
        newName = self.request.get("categoryName", None)
        maintenance_only = page_type == "maintenance"

        # The category with the new name
        categoryNewName = datastore.get_category_by_name(user.user_id(), newName, maintenance_only)

        if action == "add" and newName:
            if not categoryNewName:
                # this is a new category, add it to the database
                newCategoryObj = models.ExpenseCategory()
                if maintenance_only:
                    newCategoryObj.category = "Maintenance"
                    newCategoryObj.subcategory = newName
                else:
                    newCategoryObj.category = newName

                newCategoryObj.owner = user.user_id()
                newCategoryObj.put()
            else:
                logging.warn("User tried to add category that already exists")

        elif action == "edit" and newName:
            # Edit record

            # The category we are trying to edit
            categoryToEdit = datastore.get_category_by_id(user.user_id(), category_id)

            # If we have a category for the given id and we don't have a category
            # with the new name, update the category
            if categoryToEdit and not categoryNewName:
                if categoryToEdit.category == "Maintenance":
                    categoryToEdit.subcategory = newName
                else:
                    categoryToEdit.category = newName

                categoryToEdit.put()
            else:
                # TODO: need a way to give user feedback about why the record was not edited
                logging.warn("No category object was edited. Couldn't find it. Or you can't rename it to a duplicate name")

        self.redirect("/settings")

app = webapp2.WSGIApplication([
    ('/settings/?([^/]+)?/?([^/]+)?/?([^/]+)?/?(.+)?', SettingsHandler)
])
