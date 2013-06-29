#!/usr/bin/env python
from google.appengine.api import memcache, users
from google.appengine.ext import deferred
from webapp2_extras import jinja2
import fetchbase
import models
import utils
import webapp2

class AdminHandler(webapp2.RequestHandler):
    """The request handler for the /admin/([^/]+)? path """

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, filename, template_args):
          self.response.write(self.jinja2.render_template(filename, **template_args))

    def get(self, method):
        """
        - If the logged in user is an admin, displays the admin page.
        - Otherwise, redirects to the root page

        Args:
            method  (optional) - ignored for get requests
        """
        if users.is_current_user_admin():
            context = utils.get_context()

            self.render_template('admin.html', context)
        else:
            self.redirect("/")

    def post(self, method):
        """Post request handler for the /admin/([^/])? path

        Args:
            method  (optional) - the operation to perform
                - fetchvehicleinfo - gets car data from Cars.com
                - deletevehicles - delete all BaseVehicle entities
                - deletecarresponsestring - delete all ServerResponseString
                - clearmemcache - clears the Memcache
        """
        if users.is_current_user_admin() and method:
            if method == "fetchvehicleinfo":
                # Start retrieving data from cars.com (in the background)
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

class CronHandler(webapp2.RequestHandler):
    """The request handler for the /cron/([^/]+) path """

    def get(self, method):
        """
        Executes the defined cron job

        Args:
            method - what cron job to run
        """
        if method == "fetch":
            fetchbase.performUpdate()

app = webapp2.WSGIApplication([
    ('/admin/?([^/]+)?', AdminHandler),
    ('/cron/([^/]+)', CronHandler)
])
