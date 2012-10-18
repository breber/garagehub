from google.appengine.api import users
import md5
import models

def get_context(list_vehicles=True):
    context = {}

    user = users.get_current_user()

    context['loginurl'] = users.create_login_url("/")
    context['logouturl'] = users.create_logout_url("/")

    if user:
        userobj = {}
        userobj['isAdmin'] = users.is_current_user_admin()
        userobj['username'] = user.nickname()
        userobj['profilePic'] = "http://www.gravatar.com/avatar/%s?s=40" % md5.new(user.email()).hexdigest()
        context['user'] = userobj
        
        if list_vehicles:
            userVehiclesQuery = models.UserVehicle.query(models.UserVehicle.owner == user.user_id())
            userVehicles = userVehiclesQuery.fetch(100)
            
            if len(userVehicles) > 0:
                context['uservehicles'] = userVehicles 
    else:
        context['user'] = None

    return context

