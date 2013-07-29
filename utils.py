#!/usr/bin/env python
from google.appengine.api import users
from google.appengine.ext import ndb
import datastore
import databaseupgrade
import datetime
import hashlib
import json
import models
import time

def get_context(list_vehicles=True):
    context = {}
    context['loginurl'] = users.create_login_url("/")
    context['logouturl'] = users.create_logout_url("/")
    context['currentYear'] = datetime.date.today().year

    user = None

    google_openid = users.get_current_user()
    if google_openid:
        user = models.User.query(models.User.google_openid == google_openid.user_id()).get()

        if not user:
            user_by_email = models.User.query(models.User.email_address == google_openid.email().lower()).get()
            if user_by_email:
                user_by_email.google_openid = google_openid.user_id()
                user_by_email.is_admin = users.is_current_user_admin()
                user_by_email.put()
                user = user_by_email
            if not user_by_email:
                key = models.User(google_openid = google_openid.user_id(),
                                  email_address = google_openid.email().lower(),
                                  is_admin = users.is_current_user_admin()).put()
                user = models.User.get_by_id(key.id())

            # Update all records in database with new id
            databaseupgrade.update_userid(google_openid.user_id(), str(user.key.id()))

    if user:
        userobj = {}
        userobj['userId'] = str(user.key.id())
        userobj['isAdmin'] = user.is_admin
        userobj['username'] = user.email_address # TODO: use name from service provider
        userobj['profilePic'] = "http://www.gravatar.com/avatar/%s?s=40" % hashlib.md5(user.email_address).hexdigest() # TODO: use image from service provider
        context['user'] = userobj

        if list_vehicles:
            userVehicles = datastore.get_all_user_vehicles(str(user.key.id()))

            if len(userVehicles) > 0:
                context['uservehicles'] = sorted(userVehicles, key=lambda UserVehicle:UserVehicle.name())

            dateNotifications = datastore.get_active_date_notifications(str(user.key.id()))
            mileNotifications = datastore.get_active_mileage_notifications(str(user.key.id()))
            newNotifications = []

            for dn in dateNotifications:
                if dn.dateLastSeen != datetime.date.today():
                    newNotifications.append(dn)
            for mn in mileNotifications:
                if mn.dateLastSeen != datetime.date.today():
                    newNotifications.append(mn)

            newNotifCount = len(newNotifications)

            totalNotifications = len(dateNotifications) + len(mileNotifications)

            if totalNotifications > 0:
                context['dateNotifications'] = dateNotifications
                context['mileNotifications'] = mileNotifications
                context['totalNotifications'] = totalNotifications
            if newNotifCount > 0:
                context['newNotifications'] = newNotifCount

    else:
        context['user'] = None

    return context

def format_int(number):
    return '{:,d}'.format(number)

def format_float(number):
    return '{:,.2f}'.format(number)

def format_date(timestamp):
    return timestamp.strftime("%Y/%m/%d")

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
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
