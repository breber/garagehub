#!/usr/bin/env python
from google.appengine.ext.webapp import template
import admin
import os
import utils
import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        context = utils.get_context()
        
        path = os.path.join(os.path.dirname(__file__), 'templates/home.html')
        self.response.out.write(template.render(path, context))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/admin/?([^/]+)?', admin.AdminHandler)
], debug=True)
