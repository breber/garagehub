#!/usr/bin/env python
from google.appengine.api import memcache, users
from google.appengine.ext import deferred
from google.appengine.ext.webapp import template
import fetchbase
import models
import os
import utils
import webapp2

class AdminHandler(webapp2.RequestHandler):
    def get(self, method):
        if users.is_current_user_admin():
            context = utils.get_context()
            
            path = os.path.join(os.path.dirname(__file__), 'templates/admin.html')
            self.response.out.write(template.render(path, context))
        else:
            self.redirect("/")

    def post(self, method):
        if users.is_current_user_admin() and method:
            if method == "fetchvehicleinfo":
                deferred.defer(fetchbase.performUpdate)

            elif method == "deletevehicles":
                # Delete all vehicles
                vehicles = models.BaseVehicle.query().fetch(1000)
                for v in vehicles:
                    v.delete()

            elif method == "deletecarresponsestring":
                # Delete all car response strings
                carResps = models.ServerResponseString.query().fetch(1000)
                for r in carResps:
                    r.delete()

            elif method == "clearmemcache":
                # Clear memcache
                memcache.Client().flush_all()
        
        # Always redirect to admin
        self.redirect("/admin")

app = webapp2.WSGIApplication([
    ('/admin/?([^/]+)?', AdminHandler)
], debug=True)
