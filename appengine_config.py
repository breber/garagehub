import os
import sys
from google.appengine.ext import vendor

vendor.add('lib')

ENDPOINTS_PROJECT_DIR = os.path.join(os.path.dirname(__file__),
                                     'endpoints-proto-datastore')
sys.path.append(ENDPOINTS_PROJECT_DIR)
