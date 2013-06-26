#!/usr/bin/env python
from webapp2_extras import jinja2
import utils
import webapp2

class ToolsHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, filename, template_args):
          self.response.write(self.jinja2.render_template(filename, **template_args))

    def get(self, page_name):
        context = utils.get_context()

        if page_name == "gasprices":
            path = 'gasprices.html'
        elif page_name == "tripplanner":
            path = 'tripplanner.html'
        else:
            self.redirect("/")
            return

        self.render_template(path, context)

app = webapp2.WSGIApplication([
    ('/tools/([^/]+)', ToolsHandler)
])
