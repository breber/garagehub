#!/usr/bin/env python
from google.appengine.api import memcache, users
from google.appengine.ext.webapp import template
import os
import utils
import webapp2

class AdminHandler(webapp2.RequestHandler):
    def get(self, method):
        if users.is_current_user_admin():
            context = utils.get_context()
            
            path = os.path.join(os.path.dirname(__file__), 'templates/admin.html')
            self.response.out.write(template.render(path, context))

    def post(self, method):
        if method:
            # Do something...
            if method == "fetchvehicleinfo":
                temp = "temp"
                # TODO: fetch vehicle inforomation from cars.com
            elif method == "deletevehicles":
                temp = "temp"
                # TODO: delete all vehicles
            elif method == "deletecarresponsestring":
                temp = "temp"
                # TODO: delete car response string
            elif method == "clearmemcache":
                memcache.Client().flush_all()
        
        # Always redirect to admin
        self.redirect("/admin")

app = webapp2.WSGIApplication([
    ('/admin/?([^/]+)?', AdminHandler)
], debug=True)
