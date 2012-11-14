#!/usr/bin/env python
from google.appengine.ext.webapp import template
import os
import utils
import webapp2
import logging

class Jamie(webapp2.RequestHandler):
    def get(self):
        variable = {}

        variable['test'] = "This is a test"
        path = os.path.join(os.path.dirname(__file__), 'templates/gasprices.html')
        self.response.out.write(template.render(path, variable))
    def post(self):
       logging.info("LOG:::::::::Trying to redirect")
       self.redirect("/")        
app = webapp2.WSGIApplication([
    ('/tools/.+', Jamie),
], debug=True)
