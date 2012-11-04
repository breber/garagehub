#!/usr/bin/env python
from google.appengine.api import users
from google.appengine.ext.webapp import template
import os
import utils
import webapp2

class SettingsHandler(webapp2.RequestHandler):
    def get(self):
        context = utils.get_context()
        
        if users.get_current_user():
            path = os.path.join(os.path.dirname(__file__), 'templates/settings.html')
            self.response.out.write(template.render(path, context))
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    ('/settings', SettingsHandler)
], debug=True)
