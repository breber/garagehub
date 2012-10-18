#!/usr/bin/env python
from google.appengine.ext.webapp import template
import os
import utils
import webapp2

class UserHandler(webapp2.RequestHandler):
    def get(self, pageName):
        context = utils.get_context()
        
        if pageName == "gasprices":
            path = os.path.join(os.path.dirname(__file__), 'templates/gasprices.html')
        elif pageName == "tripplanner":
            path = os.path.join(os.path.dirname(__file__), 'templates/tripplanner.html')
        else:
            self.redirect("/")
        
        self.response.out.write(template.render(path, context))


app = webapp2.WSGIApplication([
    ('/user/([^/]+)', UserHandler)
], debug=True)
