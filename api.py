from carhub_keys import carhubkeys
from protorpc import remote
from models import *
import auth_util
import datastore
import datetime
import endpoints
import logging

# TODO: this probably isn't the best solution, but it should work for now
def get_user_by_auth(uid):
    user = User.query(User.google_oauth == uid).get()

    if user:
        return user
    else:
        current_user = endpoints.get_current_user()
        user_by_email = User.query(User.email_address == current_user.email().lower()).get()

        if not user_by_email:
            user_by_email = User()
            user_by_email.email_address = current_user.email().lower()

        user_by_email.google_oauth = uid
        user_by_email.put()

        return user_by_email

@endpoints.api(name='carhub',version='v1',
               description='CarHub API',
               hostname='car-hub.appspot.com',
               audiences=carhubkeys.AUDIENCES,
               allowed_client_ids=carhubkeys.ALLOWED_CLIENT_IDS)
class CarHubApi(remote.Service):

    @UserVehicle.query_method(user_required=True,
                              path='vehicle/list',
                              name='vehicle.list',
                              query_fields=('order', 'pageToken', 'modified_since'))
    def VehicleList(self, query):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            return query.filter(UserVehicle.owner == str(user.key.id()))
        else:
            raise endpoints.UnauthorizedException('Unknown user.')

    @UserVehicle.method(user_required=True,
                        path='vehicle/add',
                        http_method='POST',
                        name='vehicle.add')
    def VehicleAdd(self, vehicle):
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
                        request_message=UserVehicle.ProtoModel(),
                        path='vehicle/update',
                        http_method='POST',
                        name='vehicle.update')
    def VehicleUpdate(self, request):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            try:
                # Check if we have an existing record
                id_as_long = long(request.server_id)
                existing = UserVehicle.get_by_id(id_as_long)
            except AttributeError:
                logging.warn("AttributeError...")
                existing = None

            # Build the record we are going to store
            request.server_id = None
            to_store = UserVehicle.FromMessage(request)

            # Use the same key if we have one
            if existing:
                to_store._key = existing._key

            # Fill in required fields
            to_store.owner = str(user.key.id())
            to_store.lastmodified = datetime.datetime.now()
            to_store.put()

            return to_store
        else:
            raise endpoints.UnauthorizedException('Unknown user.')

    # TODO: remove this method
    @UserVehicle.method(user_required=True,
                        request_message=UserVehicle.ProtoModel(),
                        path='vehicle/update/{server_id}',
                        http_method='POST',
                        name='vehicle.updateold')
    def VehicleUpdateOld(self, request):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            try:
                # Check if we have an existing record
                id_as_long = long(request.server_id)
                existing = UserVehicle.get_by_id(id_as_long)
            except AttributeError:
                logging.warn("AttributeError...")
                existing = None

            # Build the record we are going to store
            request.server_id = None
            to_store = UserVehicle.FromMessage(request)

            # Use the same key if we have one
            if existing:
                to_store._key = existing._key

            # Fill in required fields
            to_store.owner = str(user.key.id())
            to_store.lastmodified = datetime.datetime.now()
            to_store.put()

            return to_store
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

    @endpoints.method(UnusedRequest,
                      ActiveRecords,
                      path='vehicle/active',
                      name='vehicle.active',
                      http_method='GET')
    def VehicleActive(self, request):
        current_user = endpoints.get_current_user()
        if current_user is None:
            raise endpoints.UnauthorizedException('Invalid token.')

        auth_user_id = auth_util.get_google_plus_user_id()

        user = get_user_by_auth(auth_user_id)

        query = UserVehicle.query(UserVehicle.owner == str(user.key.id()))

        items = [str(entity.id()) for entity in query.fetch(keys_only=True)]
        return ActiveRecords(active=items)



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
                              path='expense/add',
                              http_method='POST',
                              name='expense.add')
    def ExpenseAdd(self, expense):
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
                              request_message=UserExpenseRecord.ProtoModel(),
                              path='expense/update',
                              http_method='POST',
                              name='expense.update')
    def ExpenseUpdate(self, request):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            try:
                # Check if we have an existing record
                id_as_long = long(request.server_id)
                existing = UserExpenseRecord.get_by_id(id_as_long)
            except AttributeError:
                logging.warn("AttributeError...")
                existing = None

            # Build the record we are going to store
            request.server_id = None
            to_store = UserExpenseRecord.FromMessage(request)

            # Use the same key if we have one
            if existing:
                to_store._key = existing._key

            # Fill in required fields
            to_store.owner = str(user.key.id())
            to_store.lastmodified = datetime.datetime.now()
            to_store.put()

            return to_store
        else:
            raise endpoints.UnauthorizedException('Unknown user.')

    # TODO: remove this method
    @UserExpenseRecord.method(user_required=True,
                              request_message=UserExpenseRecord.ProtoModel(),
                              path='expense/update/{server_id}',
                              http_method='POST',
                              name='expense.updateold')
    def ExpenseUpdateOld(self, request):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            try:
                # Check if we have an existing record
                id_as_long = long(request.server_id)
                existing = UserExpenseRecord.get_by_id(id_as_long)
            except AttributeError:
                logging.warn("AttributeError...")
                existing = None

            # Build the record we are going to store
            request.server_id = None
            to_store = UserExpenseRecord.FromMessage(request)

            # Use the same key if we have one
            if existing:
                to_store._key = existing._key

            # Fill in required fields
            to_store.owner = str(user.key.id())
            to_store.lastmodified = datetime.datetime.now()
            to_store.put()

            return to_store
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

    @endpoints.method(VehicleRequest,
                      ActiveRecords,
                      path='expense/active',
                      name='expense.active',
                      http_method='GET')
    def ExpenseActive(self, request):
        current_user = endpoints.get_current_user()
        if current_user is None:
            raise endpoints.UnauthorizedException('Invalid token.')

        auth_user_id = auth_util.get_google_plus_user_id()

        user = get_user_by_auth(auth_user_id)

        query = UserExpenseRecord.query(UserExpenseRecord.owner == str(user.key.id()),
                                        UserExpenseRecord.vehicle == request.vehicle)

        items = [str(entity.id()) for entity in query.fetch(keys_only=True)]
        return ActiveRecords(active=items)



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
                              path='maintenance/add',
                              http_method='POST',
                              name='maintenance.add')
    def MaintenanceAdd(self, maintenance):
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
                              request_message=MaintenanceRecord.ProtoModel(),
                              path='maintenance/update',
                              http_method='POST',
                              name='maintenance.update')
    def MaintenanceUpdate(self, request):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            try:
                # Check if we have an existing record
                id_as_long = long(request.server_id)
                existing = MaintenanceRecord.get_by_id(id_as_long)
            except AttributeError:
                logging.warn("AttributeError...")
                existing = None

            # Build the record we are going to store
            request.server_id = None
            to_store = MaintenanceRecord.FromMessage(request)

            # Use the same key if we have one
            if existing:
                to_store._key = existing._key

            # Fill in required fields
            to_store.owner = str(user.key.id())
            to_store.lastmodified = datetime.datetime.now()
            to_store.put()

            return to_store
        else:
            raise endpoints.UnauthorizedException('Unknown user.')

    # TODO: remove this method
    @MaintenanceRecord.method(user_required=True,
                              request_message=MaintenanceRecord.ProtoModel(),
                              path='maintenance/update/{server_id}',
                              http_method='POST',
                              name='maintenance.updateold')
    def MaintenanceUpdateOld(self, request):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            try:
                # Check if we have an existing record
                id_as_long = long(request.server_id)
                existing = MaintenanceRecord.get_by_id(id_as_long)
            except AttributeError:
                logging.warn("AttributeError...")
                existing = None

            # Build the record we are going to store
            request.server_id = None
            to_store = MaintenanceRecord.FromMessage(request)

            # Use the same key if we have one
            if existing:
                to_store._key = existing._key

            # Fill in required fields
            to_store.owner = str(user.key.id())
            to_store.lastmodified = datetime.datetime.now()
            to_store.put()

            return to_store
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

    @endpoints.method(VehicleRequest,
                      ActiveRecords,
                      path='maintenance/active',
                      name='maintenance.active',
                      http_method='GET')
    def MaintenanceActive(self, request):
        current_user = endpoints.get_current_user()
        if current_user is None:
            raise endpoints.UnauthorizedException('Invalid token.')

        auth_user_id = auth_util.get_google_plus_user_id()

        user = get_user_by_auth(auth_user_id)

        query = MaintenanceRecord.query(MaintenanceRecord.owner == str(user.key.id()),
                                        MaintenanceRecord.vehicle == request.vehicle)

        items = [str(entity.id()) for entity in query.fetch(keys_only=True)]
        return ActiveRecords(active=items)



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
                       path='fuel/add',
                       http_method='POST',
                       name='fuel.add')
    def FuelAdd(self, fuel):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            fuel.categoryid = datastore.get_category_by_name(str(user.key.id()), "Fuel Up").key.id()
            fuel.description = "Filled up with gas"
            fuel.owner = str(user.key.id())
            fuel.lastmodified = datetime.datetime.now()
            fuel.put()
            return fuel
        else:
            raise endpoints.UnauthorizedException('Unknown user.')

    @FuelRecord.method(user_required=True,
                       request_message=FuelRecord.ProtoModel(),
                       path='fuel/update',
                       http_method='POST',
                       name='fuel.update')
    def FuelUpdate(self, request):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            try:
                # Check if we have an existing record
                id_as_long = long(request.server_id)
                existing = FuelRecord.get_by_id(id_as_long)
            except AttributeError:
                logging.warn("AttributeError...")
                existing = None

            # Build the record we are going to store
            request.server_id = None
            to_store = FuelRecord.FromMessage(request)

            # Use the same key if we have one
            if existing:
                to_store._key = existing._key

            # Fill in required fields
            to_store.categoryid = datastore.get_category_by_name(str(user.key.id()), "Fuel Up").key.id()
            to_store.description = "Filled up with gas"
            to_store.owner = str(user.key.id())
            to_store.lastmodified = datetime.datetime.now()
            to_store.put()

            return to_store
        else:
            raise endpoints.UnauthorizedException('Unknown user.')

    # TODO: remove this method
    @FuelRecord.method(user_required=True,
                       request_message=FuelRecord.ProtoModel(),
                       path='fuel/update/{server_id}',
                       http_method='POST',
                       name='fuel.updateold')
    def FuelUpdateOld(self, request):
        auth_user_id = auth_util.get_google_plus_user_id()
        user = get_user_by_auth(auth_user_id)

        if user:
            try:
                # Check if we have an existing record
                id_as_long = long(request.server_id)
                existing = FuelRecord.get_by_id(id_as_long)
            except AttributeError:
                logging.warn("AttributeError...")
                existing = None

            # Build the record we are going to store
            request.server_id = None
            to_store = FuelRecord.FromMessage(request)

            # Use the same key if we have one
            if existing:
                to_store._key = existing._key

            # Fill in required fields
            to_store.categoryid = datastore.get_category_by_name(str(user.key.id()), "Fuel Up").key.id()
            to_store.description = "Filled up with gas"
            to_store.owner = str(user.key.id())
            to_store.lastmodified = datetime.datetime.now()
            to_store.put()

            return to_store
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

    @endpoints.method(VehicleRequest,
                      ActiveRecords,
                      path='fuel/active',
                      name='fuel.active',
                      http_method='GET')
    def FuelActive(self, request):
        current_user = endpoints.get_current_user()
        if current_user is None:
            raise endpoints.UnauthorizedException('Invalid token.')

        auth_user_id = auth_util.get_google_plus_user_id()

        user = get_user_by_auth(auth_user_id)

        query = FuelRecord.query(FuelRecord.owner == str(user.key.id()),
                                 FuelRecord.vehicle == request.vehicle)

        items = [str(entity.id()) for entity in query.fetch(keys_only=True)]
        return ActiveRecords(active=items)



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
