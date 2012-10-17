from google.appengine.api import users
import md5

def get_context():
    context = {}

    user = users.get_current_user()

    context['loginurl'] = users.create_login_url("/")
    context['logouturl'] = users.create_logout_url("/")

    if user:
        userobj = {}
        userobj['isAdmin'] = users.is_current_user_admin()
        userobj['username'] = user.nickname()
        userobj['md5'] = md5.new(user.email()).hexdigest()
        context['user'] = userobj
    else:
        context['user'] = None

    return context
