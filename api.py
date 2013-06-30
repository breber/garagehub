from google.appengine.ext import endpoints
from protorpc import remote
from models import *
import auth_util
import datetime
import logging

ANDROID_CLIENT_ID = '280486107933.apps.googleusercontent.com'
ANDROID_DEBUG_CLIENT_ID = '280486107933-4r3v4nis34qimv27bc3pb8vppk38nvho.apps.googleusercontent.com'
CLIENT_ID = '280486107933-fkp13pk6dv84vdkumqu1vj5hh0o74he3.apps.googleusercontent.com'

# TODO: this probably isn't the best solution, but it should work for now
def get_user_by_auth(uid):
    user = User.query(User.google_oauth == uid).get()

    if user:
        return user
    else:
        current_user = endpoints.get_current_user()
        user_by_email = User.query(User.email_address == current_user.email()).get()

        if user_by_email:
            user_by_email.google_oauth = uid
            user_by_email.put()

        return user_by_email

@endpoints.api(name='carhub',version='v1',
               description='CarHub API',
               hostname='car-hub.appspot.com',
               audiences=[CLIENT_ID, ANDROID_CLIENT_ID, ANDROID_DEBUG_CLIENT_ID],
               allowed_client_ids=[ANDROID_CLIENT_ID, ANDROID_DEBUG_CLIENT_ID, CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class CarHubApi(remote.Service):

    @UserVehicle.query_method(user_required=True,
                              path='vehicle/list',
                              name='vehicle.list')
    def VehicleList(self, query):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            return query.filter(UserVehicle.owner == str(user.key.id()))
        else:
            raise endpoints.UnauthorizedException('Unknown user.')

    @UserVehicle.method(user_required=True,
                        path='vehicle/store',
                        http_method='POST',
                        name='vehicle.store')
    def VehicleStore(self, vehicle):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            vehicle.owner = str(user.key.id())
            vehicle.lastmodified = datetime.datetime.now()
            vehicle.put()
            return vehicle
        else:
            raise endpoints.UnauthorizedException('Unknown user.')

    @UserVehicle.method(user_required=True,
                        path='vehicle/delete',
                        http_method='POST',
                        name='vehicle.delete')
    def VehicleDelete(self, vehicle):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            server_vehicle = UserVehicle.get_by_id(vehicle.key.id())
            if server_vehicle and server_vehicle.owner == str(user.key.id()):
                server_vehicle.key.delete()
                return True

            return False
        else:
            raise endpoints.UnauthorizedException('Unknown user.')



    @UserExpenseRecord.query_method(user_required=True,
                                    path='expense/list/{vehicle}',
                                    name='expense.list',
                                    http_method='GET',
                                    query_fields=('vehicle', 'order', 'pageToken', 'modified_since'))
    def ExpenseList(self, query):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            return query.filter(UserExpenseRecord.owner == str(user.key.id()))
        else:
            raise endpoints.UnauthorizedException('Unknown user.')

    @UserExpenseRecord.method(user_required=True,
                              path='expense/store',
                              http_method='POST',
                              name='expense.store')
    def ExpenseStore(self, expense):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            expense.owner = str(user.key.id())
            expense.lastmodified = datetime.datetime.now()
            expense.put()
            return expense
        else:
            raise endpoints.UnauthorizedException('Unknown user.')

    @UserExpenseRecord.method(user_required=True,
                              path='expense/delete',
                              http_method='POST',
                              name='expense.delete')
    def ExpenseDelete(self, expense):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            server_expense = UserExpenseRecord.get_by_id(expense.key.id())
            if server_expense and server_expense.owner == str(user.key.id()):
                server_expense.key.delete()
                return True

            return False
        else:
            raise endpoints.UnauthorizedException('Unknown user.')



    @MaintenanceRecord.query_method(user_required=True,
                                    path='maintenance/list/{vehicle}',
                                    name='maintenance.list',
                                    http_method='GET',
                                    query_fields=('vehicle', 'order', 'pageToken', 'modified_since'))
    def MaintenanceList(self, query):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            return query.filter(MaintenanceRecord.owner == str(user.key.id()))
        else:
            raise endpoints.UnauthorizedException('Unknown user.')

    @MaintenanceRecord.method(user_required=True,
                              path='maintenance/store',
                              http_method='POST',
                              name='maintenance.store')
    def MaintenanceStore(self, maintenance):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            maintenance.owner = str(user.key.id())
            maintenance.lastmodified = datetime.datetime.now()
            maintenance.put()
            return maintenance
        else:
            raise endpoints.UnauthorizedException('Unknown user.')

    @MaintenanceRecord.method(user_required=True,
                              path='maintenance/delete',
                              http_method='POST',
                              name='maintenance.delete')
    def MaintenanceDelete(self, maintenance):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            server_maintenance = MaintenanceRecord.get_by_id(maintenance.key.id())
            if server_maintenance and server_maintenance.owner == str(user.key.id()):
                server_maintenance.key.delete()
                return True

            return False
        else:
            raise endpoints.UnauthorizedException('Unknown user.')



    @FuelRecord.query_method(user_required=True,
                             path='fuel/list/{vehicle}',
                             name='fuel.list',
                             http_method='GET',
                             query_fields=('vehicle', 'order', 'pageToken', 'modified_since'))
    def FuelList(self, query):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            return query.filter(FuelRecord.owner == str(user.key.id()))
        else:
            raise endpoints.UnauthorizedException('Unknown user.')

    @FuelRecord.method(user_required=True,
                       path='fuel/store',
                       http_method='POST',
                       name='fuel.store')
    def FuelStore(self, fuel):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            fuel.categoryid = datastore.get_category_by_name(user_id, "Fuel Up").key.id()
            fuel.description = "Filled up with gas"
            fuel.owner = str(user.key.id())
            fuel.lastmodified = datetime.datetime.now()
            fuel.put()
            return fuel
        else:
            raise endpoints.UnauthorizedException('Unknown user.')

    @FuelRecord.method(user_required=True,
                       path='fuel/delete',
                       http_method='POST',
                       name='fuel.delete')
    def FuelDelete(self, fuel):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            server_fuel = FuelRecord.get_by_id(fuel.key.id())
            if server_fuel and server_fuel.owner == str(user.key.id()):
                server_fuel.key.delete()
                return True

            return False
        else:
            raise endpoints.UnauthorizedException('Unknown user.')



    @ExpenseCategory.query_method(user_required=True,
                                  path='category/list',
                                  name='category.list',
                                  http_method='GET',
                                  query_fields=('pageToken',))
    def CategoryList(self, query):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            users = [str(user.key.id()), "defaultCategory", "defaultMaintCategory"]

            return query.filter(ExpenseCategory.owner.IN(users)).order(ExpenseCategory._key)
        else:
            raise endpoints.UnauthorizedException('Unknown user.')

application = endpoints.api_server([CarHubApi], restricted=False)
