#!/usr/bin/env python

from google.appengine.ext import ndb
import datastore
import models

def update_userid(old, new):
    # Update uservehicle
    user_vehicles = datastore.get_all_user_vehicles(old)
    for veh in user_vehicles:
        veh.owner = new
        veh.put()

        # Update all expenses
        user_expenses = datastore.get_all_expense_records(old, veh.key.id(), day_range=5000)
        for exp in user_expenses:
            exp.owner = new
            exp.put()

    # Update maintenance categories
    maint_cat = datastore.get_maintenance_categories(old, default_categories=False)
    for cat in maint_cat:
        cat.owner = new
        cat.put()

    # Update expense categories
    exp_cat = datastore.get_expense_categories(old, default_categories=False)
    for cat in exp_cat:
        cat.owner = new
        cat.put()
