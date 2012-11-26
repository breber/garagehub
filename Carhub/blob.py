#!/usr/bin/env python
from google.appengine.api import users
from google.appengine.ext.webapp import template

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


import datastore
import datetime
import logging
import models
import os
import utils
import webapp2
import urllib

class picture_view(blobstore_handlers.BlobstoreDownloadHandler):
    
    def get(self, blob_key):
        blob_key = str(urllib.unquote(blob_key))
        if not blobstore.get(blob_key):
            self.error(404)
        else:
            self.send_blob(blobstore.BlobInfo.get(blob_key))
            
app = webapp2.WSGIApplication([                  
    ('/blob/([^/]+)', picture_view)
], debug=True)