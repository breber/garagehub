'''
Created on Dec 10, 2012

@author: breber
'''

from google.appengine.api import images
from google.appengine.ext import ndb
import logging
import models
import webapp2

#class DatabaseUpgrade(webapp2.RequestHandler):
#    def get(self):
#        query = models.BaseExpense().query()
#        expenses = ndb.get_multi(query.fetch(keys_only=True))
#        
#        for e in expenses:
#            if e.picture:
#                e.pictureurl = images.get_serving_url(e.picture, 400)
#                logging.warn("%s" % e.pictureurl)
#                e.put()
#        
#        self.redirect("/")
#
#app = webapp2.WSGIApplication([ 
#    ('/database/upgrade', DatabaseUpgrade),
#], debug=True)
