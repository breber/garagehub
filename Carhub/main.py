#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext.webapp import template
import os
import utils
import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        context = utils.get_context()
        
#        if context['username']:
#            path = os.path.join(os.path.dirname(__file__), 'templates/shows.html')
#        else:
        path = os.path.join(os.path.dirname(__file__), 'templates/home.html')

        self.response.out.write(template.render(path, context))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
