#!/usr/bin/env python
from google.appengine.ext.webapp import template
import os
import utils
import webapp2

class ToolsHandler(webapp2.RequestHandler):
    def get(self, page_name):
        context = utils.get_context()

        if page_name == "gasprices":
            path = os.path.join(os.path.dirname(__file__), 'templates/gasprices.html')
        elif page_name == "tripplanner":
            path = os.path.join(os.path.dirname(__file__), 'templates/tripplanner.html')
        else:
            self.redirect("/")

        self.response.out.write(template.render(path, context))

app = webapp2.WSGIApplication([
    ('/tools/([^/]+)', ToolsHandler)
])
