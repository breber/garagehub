#!/usr/bin/env python
from google.appengine.api import urlfetch
import json
import webapp2

class FuelRequestHandler(webapp2.RequestHandler):
    def get(self, lat, lon, radius):
        self.response.headerlist = [('Content-type', 'application/json')]

        url = 'http://api.mygasfeed.com/stations/radius/%f/%f/%d/%s/%s/zax22arsix.json' % (float(lat), float(lon), int(radius), 'reg', 'price')
        result = urlfetch.fetch(url=url, payload=None, method=urlfetch.GET, deadline=30)

        stations = []
        if result.status_code == 200:
            json_result = json.loads(result.content)
            json_stations = json_result['stations']

            for s in json_stations:
                station = {}
                station['price'] = s['reg_price']
                station['address'] = s['address']
                station['station'] = s['station']
                station['city'] = s['city']
                stations.append(station)

        data = {}
        data['stations'] = stations

        self.response.out.write(json.dumps(data))

app = webapp2.WSGIApplication([
    ('/fuel/(.+?)?/(.+?)?/(.+?)?', FuelRequestHandler)
])
