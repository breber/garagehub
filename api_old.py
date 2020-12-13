#!/usr/bin/env python
from google.appengine.api import users
from flask import Flask, make_response, render_template
import datastore
import json
import models
import utils

app = Flask(__name__)

@app.route('/api/expense/category/<vehicle_id>', defaults={'last_modified': "0"})
@app.route('/api/expense/category/<vehicle_id>/<last_modified>')
def expense_category(vehicle_id, last_modified=0):
    context = utils.get_context()
    user_id = context['user']['userId']
    baseexpenses = datastore.get_all_expense_records(user_id, vehicle_id, long(last_modified))

    toRet = {}

    for record in baseexpenses:
        category = datastore.get_category_by_id(record.owner, record.categoryid).category
        prev = 0
        if category in toRet.keys():
            prev = toRet[category]
        toRet[category] = prev + record.amount

    toRet1 = []
    for cat in toRet.keys():
        category = []
        category.append(cat)
        category.append(toRet[cat])
        toRet1.append(category)

    return toRet1
