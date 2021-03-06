# For the generateendpoints.sh script, we need to add the subdirectory
# into our path
if 0:
    import sys
    sys.path.append('endpoints-proto-datastore')

from datetime import datetime
from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from protorpc import remote, messages
from endpoints_proto_datastore.ndb import EndpointsModel, EndpointsAliasProperty, EndpointsVariantIntegerProperty

import endpoints
import utils

class User(ndb.Model):
    email_address = ndb.StringProperty()
    is_admin = ndb.BooleanProperty(default=False)
    google_openid = ndb.StringProperty()
    google_oauth = ndb.StringProperty()
    mobile_ids = ndb.StringProperty(repeated=True)  # For Google Cloud Messaging

class UserVehicle(EndpointsModel):
    _message_fields_schema = ('server_id', 'make', 'model', 'year', 'color', 'plates', 'lastmodified')

    make = ndb.StringProperty()
    model = ndb.StringProperty()
    owner = ndb.StringProperty()
    year = ndb.StringProperty()
    color = ndb.StringProperty()
    plates = ndb.StringProperty()
    lastmodified = ndb.DateTimeProperty()

    @EndpointsAliasProperty(property_type=messages.StringField)
    def server_id(self):
        return str(self.key.id())

    def modified_since_set(self, value):
        try:
            modified_since = datetime.fromtimestamp(long(value) / 1000)
            if not isinstance(modified_since, datetime):
                raise TypeError('Not a datetime stamp.')
        except TypeError:
            raise endpoints.BadRequestException('Invalid timestamp for modifiedSince.')

        self._endpoints_query_info._filters.add(UserVehicle.lastmodified >= modified_since)

    @EndpointsAliasProperty(setter=modified_since_set)
    def modified_since(self):
        raise endpoints.BadRequestException('modifiedSince value should never be accessed.')

    def name(self):
        return "%s %s %s" % (self.year, self.make, self.model)

class ExpenseCategory(EndpointsModel):
    _message_fields_schema = ('server_id', 'category', 'subcategory')

    owner = ndb.StringProperty()
    category = ndb.StringProperty()
    subcategory = ndb.StringProperty()

    @EndpointsAliasProperty(property_type=messages.StringField)
    def server_id(self):
        return str(self.key.id())

    def name(self):
        if self.subcategory:
            return self.subcategory

        return self.category

class BaseExpense(EndpointsModel, polymodel.PolyModel):
    _message_fields_schema = ('server_id', 'vehicle', 'date', 'lastmodified', 'categoryid', 'location', 'description', 'amount', 'pictureurl')

    owner = ndb.StringProperty()
    vehicle = ndb.IntegerProperty()
    date = ndb.DateProperty()
    lastmodified = ndb.DateTimeProperty()
    categoryid = ndb.IntegerProperty()
    location = ndb.StringProperty()
    description = ndb.StringProperty()
    amount = ndb.FloatProperty()
    picture = ndb.StringProperty()
    pictureurl = ndb.StringProperty()

    @EndpointsAliasProperty(property_type=messages.StringField)
    def server_id(self):
        return str(self.key.id())

    def modified_since_set(self, value):
        try:
            modified_since = datetime.fromtimestamp(long(value) / 1000)
            if not isinstance(modified_since, datetime):
                raise TypeError('Not a datetime stamp.')
        except TypeError:
            raise endpoints.BadRequestException('Invalid timestamp for modifiedSince.')

        self._endpoints_query_info._filters.add(BaseExpense.lastmodified >= modified_since)

    @EndpointsAliasProperty(setter=modified_since_set)
    def modified_since(self):
        raise endpoints.BadRequestException('modifiedSince value should never be accessed.')

    def date_formatted(self):
        return utils.format_date(self.date)

    def amount_formatted(self):
        return utils.format_float(self.amount)

    def name(self):
        return "%s %s %s %s" % (self.date, self.location, self.category, self.amount)

    # ENDPOINTS STUFF
    from endpoints_polymodel import _PolyModelQueryInfo, _DowncastMessage
    def __init__(self, *args, **kwargs):
        from endpoints_polymodel import _PolyModelQueryInfo
        # Don't need to call both constructors since PolyModel doesn't define one
        # and descends from model.Model, a superclass of EndpointsModel
        super(BaseExpense, self).__init__(*args, **kwargs)
        self._endpoints_query_info = _PolyModelQueryInfo(self)

    @classmethod
    def ToMessageCollection(cls, items, collection_fields=None,
                            next_cursor=None):
        from endpoints_polymodel import _DowncastMessage
        proto_model = cls.ProtoCollection(collection_fields=collection_fields)

        items_as_message = [item.ToMessage(fields=collection_fields)
                            for item in items]
        final_proto_class = cls.ProtoModel(fields=collection_fields)
        items_as_message = [_DowncastMessage(item, final_proto_class)
                            for item in items_as_message]

        result = proto_model(items=items_as_message)

        if next_cursor is not None:
            result.nextPageToken = next_cursor.to_websafe_string()

        return result

class UserExpenseRecord(BaseExpense):
    _message_fields_schema = ('server_id', 'vehicle', 'date', 'lastmodified', 'categoryid', 'location', 'description', 'amount', 'pictureurl')

class MaintenanceRecord(BaseExpense):
    _message_fields_schema = ('server_id', 'vehicle', 'date', 'lastmodified', 'categoryid', 'location', 'description', 'amount', 'pictureurl', 'odometer')

    odometer = EndpointsVariantIntegerProperty(variant=messages.Variant.INT32)

    def odometer_formatted(self):
        if utils.format_int(self.odometer) == "-1":
            return ""
        return utils.format_int(self.odometer)

class FuelRecord(BaseExpense):
    _message_fields_schema = ('server_id', 'vehicle', 'date', 'lastmodified', 'categoryid', 'location', 'description', 'amount', 'pictureurl', 'mpg', 'odometerStart', 'odometerEnd', 'gallons', 'costPerGallon', 'fuelGrade')

    mpg = ndb.FloatProperty()
    odometerStart = EndpointsVariantIntegerProperty(variant=messages.Variant.INT32)
    odometerEnd = EndpointsVariantIntegerProperty(variant=messages.Variant.INT32)
    gallons = ndb.FloatProperty()
    costPerGallon = ndb.FloatProperty()
    fuelGrade = ndb.StringProperty()

    def mpg_formatted(self):
        return utils.format_float(self.mpg)

    def odometerStart_formatted(self):
        return utils.format_int(self.odometerStart)

    def odometerEnd_formatted(self):
        return utils.format_int(self.odometerEnd)

    def gallons_formatted(self):
        return utils.format_float(self.gallons)

    def costPerGallon_formatted(self):
        return utils.format_float(self.costPerGallon)


# API specific messages
class UnusedRequest(messages.Message):
    unused = messages.StringField(1, required=False)

class StringRequest(messages.Message):
    string = messages.StringField(1, required=True)

class VehicleRequest(messages.Message):
    vehicle = messages.IntegerField(1, required=True)

class ActiveRecords(messages.Message):
    active = messages.StringField(1, repeated=True)
