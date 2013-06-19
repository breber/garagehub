from google.appengine.ext import endpoints
from protorpc import remote
from models import *

CLIENT_ID = '280486107933.apps.googleusercontent.com'

@endpoints.api(name='carhub',version='v1',
               description='CarHub API',
               hostname='car-hub.appspot.com',
               audiences=[CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               allowed_client_ids=[CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class CarHubApi(remote.Service):

    @UserVehicle.query_method(path='vehicles', name='vehicles.list')
    def VehiclesList(self, query):
        return query

application = endpoints.api_server([CarHubApi], restricted=False)
