from google.appengine.api import users
from google.appengine.ext import ndb
import datastore
import datetime
import hashlib
import json
import time

def get_context(list_vehicles=True):
    context = {}
    context['loginurl'] = users.create_login_url("/")
    context['logouturl'] = users.create_logout_url("/")
    context['currentYear'] = datetime.date.today().year

    user = users.get_current_user()
    if user:
        userobj = {}
        userobj['isAdmin'] = users.is_current_user_admin()
        userobj['username'] = user.nickname()
        userobj['profilePic'] = "http://www.gravatar.com/avatar/%s?s=40" % hashlib.md5(user.email()).hexdigest()
        context['user'] = userobj

        if list_vehicles:
            userVehicles = datastore.get_all_user_vehicles(user.user_id())

            if len(userVehicles) > 0:
                context['uservehicles'] = sorted(userVehicles, key=lambda UserVehicle:UserVehicle.name())

            dateNotifications = datastore.get_active_date_notifications(user.user_id())
            mileNotifications = datastore.get_active_mileage_notifications(user.user_id())
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
