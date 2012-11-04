#!/usr/bin/env python
from google.appengine.api import users
import datastore
import json
import webapp2

class FuelHandler(webapp2.RequestHandler):
    def get(self, vehicleId, day_range):
        self.response.headerlist = [('Content-type', 'application/json')]
        
        user = users.get_current_user()
        
        if user:
            if day_range:
                results = datastore.getFuelRecords(user.user_id(), vehicleId, long(day_range))
            else:
                results = datastore.getFuelRecords(user.user_id(), vehicleId)
            
            self.response.out.write(json.dumps(results))


app = webapp2.WSGIApplication([
    ('/api/fuel/([^/]+)/?(.+?)?', FuelHandler),
], debug=True)
