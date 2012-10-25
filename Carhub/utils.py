from google.appengine.api import users
from google.appengine.ext import ndb
import hashlib
import models


def get_context(list_vehicles=True):
    context = {}
    context['loginurl'] = users.create_login_url("/")
    context['logouturl'] = users.create_logout_url("/")

    user = users.get_current_user()
    if user:
        userobj = {}
        userobj['isAdmin'] = users.is_current_user_admin()
        userobj['username'] = user.nickname()
        userobj['profilePic'] = "http://www.gravatar.com/avatar/%s?s=40" % hashlib.md5(user.email()).hexdigest()
        context['user'] = userobj
        
        if list_vehicles:
            userVehiclesQuery = models.UserVehicle.query(models.UserVehicle.owner == user.user_id())
            userVehicles = ndb.get_multi(userVehiclesQuery.fetch(keys_only=True))
            
            if len(userVehicles) > 0:
                context['uservehicles'] = userVehicles 

        #TODO this needs to grab based on vehicle chosen also
        userExpensesQuery = models.UserExpense.query(models.UserExpense.owner == user.user_id())
        userExpenses = ndb.get_multi(userExpensesQuery.fetch(keys_only=True))
        if len(userExpenses) > 0:
                context['userexpenses'] = userExpenses 
        
    else:
        context['user'] = None

    return context

