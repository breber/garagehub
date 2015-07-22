#!/usr/bin/env python
from garagehub_keys import garagehubkeys
from google.appengine.api import urlfetch, users
import base64
import datastore
import json
import urllib
import utils
import webapp2

class NewsHandler(webapp2.RequestHandler):
    def get(self, vehicle_id):
        context = utils.get_context()
        user_id = context['user']['userId']
        self.response.headerlist = [('Content-type', 'application/json')]

        output = {}

        # If the path doesn't contain a first parameter, just show the garage
        if not vehicle_id:
            output['error'] = 'missing vehicle id'

        # If we have a first path parameter, and it isn't add, use that as
        # the vehicle ID and show that vehicle's page
        else:
            car = datastore.get_user_vehicle(user_id, vehicle_id)

            if car:
                auth_key = base64.b64encode('$acctKey:%s' % garagehubkeys.BING_SEARCH_KEY)
                search_str = urllib.quote('%s %s %s' % (car.year, car.make, car.model))
                api_url = 'https://api.datamarket.azure.com/Bing/Search/v1/News?Query=\'%s\'&$format=json' % search_str

                result = urlfetch.fetch(url=api_url, headers={ 'Authorization': 'Basic %s' % auth_key })

                if result.status_code == 200:
                    self.response.out.write(result.content)
                    return
                else:
                    output['error'] = 'error fetching search results'
            else:
                output['error'] = 'invalid vehicle id'

        self.response.out.write(json.dumps(output))

app = webapp2.WSGIApplication([
    ('/news/([^/]+)', NewsHandler),
], debug=True)
