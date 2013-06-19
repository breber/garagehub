from google.appengine.ext import endpoints
from protorpc import remote
from models import *
import logging

ANDROID_CLIENT_ID = '280486107933.apps.googleusercontent.com'
ANDROID_DEBUG_CLIENT_ID = '280486107933-4r3v4nis34qimv27bc3pb8vppk38nvho.apps.googleusercontent.com'
CLIENT_ID = '280486107933-fkp13pk6dv84vdkumqu1vj5hh0o74he3.apps.googleusercontent.com'

@endpoints.api(name='carhub',version='v1',
               description='CarHub API',
               hostname='car-hub.appspot.com',
               audiences=[CLIENT_ID, ANDROID_CLIENT_ID, ANDROID_DEBUG_CLIENT_ID],
               allowed_client_ids=[ANDROID_CLIENT_ID, ANDROID_DEBUG_CLIENT_ID, CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class CarHubApi(remote.Service):

    @UserVehicle.query_method(user_required=True, path='vehicles', name='vehicles.list')
    def VehiclesList(self, query):
        logging.warn("User: %s" % endpoints.get_current_user())
        return query.filter(UserVehicle.owner == endpoints.get_current_user().user_id())

application = endpoints.api_server([CarHubApi], restricted=False)
