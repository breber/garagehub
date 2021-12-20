#!/usr/bin/env python
from google.appengine.api import users
from flask import Flask, make_response, Response
import datastore
import json
import models
import utils

app = Flask(__name__)

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        from google.appengine.ext import ndb
        import datetime
        import time

        if isinstance(obj, datetime.datetime):
            return time.mktime(obj.timetuple())
        elif isinstance(obj, datetime.date):
            toRet = {}
            toRet["timestamp"] = time.mktime(obj.timetuple())
            toRet["str"] = obj.strftime("%m/%d/%y")
            return toRet
        elif isinstance(obj, ndb.Model):
            toRet = obj.to_dict()
            toRet["id"] = obj.key.id()
            return toRet
        elif isinstance(obj, ndb.Key):
            return obj.id()

        return json.JSONEncoder.default(self, obj)


@app.route('/api/vehicle/list')
def vehicles():
    context = utils.get_context()
    user_id = context['user']['userId']

    results = datastore.get_all_user_vehicles(user_id)

    toRet = {}
    toRet["records"] = results

    return Response(json.dumps(toRet, cls=ComplexEncoder), mimetype='application/json')


@app.route('/api/fuel/<vehicle_id>')
def fuels(vehicle_id):
    context = utils.get_context()
    user_id = context['user']['userId']

    fuels = datastore.get_fuel_records(user_id, vehicle_id, day_range=None)

    toRet = {}
    toRet["records"] = fuels

    return Response(json.dumps(toRet, cls=ComplexEncoder), mimetype='application/json')


@app.route('/api/maintenance/<vehicle_id>')
def maintenances(vehicle_id):
    context = utils.get_context()
    user_id = context['user']['userId']

    maints = datastore.get_maintenance_records(user_id, vehicle_id, day_range=None)

    categories = {}

    for record in maints:
        category = datastore.get_category_by_id(record.owner, record.categoryid)
        if category:
            if category.subcategory:
                categories[record.categoryid] = category.subcategory
            else:
                categories[record.categoryid] = category.category

    toRet = {}
    toRet["records"] = maints
    toRet["categories"] = categories

    return Response(json.dumps(toRet, cls=ComplexEncoder), mimetype='application/json')


@app.route('/api/expense/fuel/<vehicle_id>', defaults={'last_modified': "0"})
@app.route('/api/expense/fuel/<vehicle_id>/<last_modified>')
def expense_fuel(vehicle_id, last_modified=0):
    context = utils.get_context()

    user_id = context['user']['userId']
    results = datastore.get_fuel_records(user_id, vehicle_id, long(last_modified))

    toRet = {}
    toRet["activeIds"] = models.FuelRecord.query(models.FuelRecord.owner == user_id).fetch(keys_only=True)
    toRet["records"] = results

    resp = make_response(json.dumps(toRet, cls=ComplexEncoder))
    resp.headers['Content-type'] = 'application/json'
    return resp

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

    return { 'data': toRet1 }
