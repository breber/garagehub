from google.appengine.api import users

def get_context():
    context = {}

    user = users.get_current_user()

    context['loginurl'] = users.create_login_url("/")
    context['logouturl'] = users.create_logout_url("/")

    if user:
        context['username'] = user.nickname()
    else:
        context['username'] = None

    return context
