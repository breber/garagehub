from google.appengine.api import users
import hashlib
import datastore

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
            userVehicles = datastore.getUserVehicleList(user.user_id())
            
            if len(userVehicles) > 0:
                context['uservehicles'] = sorted(userVehicles, key=lambda UserVehicle:UserVehicle.name())
            
            notifications = datastore.getNotifications(user.user_id())
            
            if len(notifications) > 0:
                context['notifications'] = notifications
        
    else:
        context['user'] = None

    return context

