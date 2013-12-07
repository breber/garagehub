from carhub_keys import carhubkeys
from datetime import datetime, timedelta
import logging
import models
import re
import urllib, urllib2
import json

from google.appengine.api import taskqueue  ## Google App Engine specific

LOCALHOST = False

GOOGLE_LOGIN_URL = 'https://www.google.com/accounts/ClientLogin'
# Can't use https on localhost due to Google cert bug
GOOGLE_GCM_SEND_URL = 'http://android.apis.google.com/gcm/send' if LOCALHOST \
else 'https://android.apis.google.com/gcm/send'
GOOGLE_GCM_SEND_URL = 'http://android.googleapis.com/gcm/send' if LOCALHOST \
else 'https://android.googleapis.com/gcm/send'

TOTAL_ERRORS = 'total_errors'
TOTAL_MESSAGES = 'total_messages'

class GCMMessage:
    user = None
    notification = None
    collapse_key = None
    delay_while_idle = None
    time_to_live = None

    def __init__(self, user, notification="", collapse_key=None, delay_while_idle=None, time_to_live=None):
        if len(user.mobile_ids) > 0:
            self.user = user

        self.notification = notification
        self.collapse_key = collapse_key
        self.delay_while_idle = delay_while_idle
        self.time_to_live = time_to_live

    def __unicode__(self):
        return "%s:%s:%s:%s:%s" % (repr(self.user),
                                   repr(self.notification),
                                   repr(self.collapse_key),
                                   repr(self.delay_while_idle),
                                   repr(self.time_to_live))

    def json_string(self):
        if not self.user:
            logging.error('GCMMessage generate_json_string error. Invalid device tokens: ' + repr(self))
            raise Exception('GCMMessage generate_json_string error. Invalid device tokens.')

        json_dict = {}
        json_dict['registration_ids'] = self.user.mobile_ids

        # If message is a dict, send each key individually
        # Else, send entire message under data key
        if isinstance(self.notification, dict):
            json_dict['data'] = self.notification
        else:
            json_dict['data'] = {'data': self.notification}

        if self.collapse_key:
            json_dict['collapse_key'] = self.collapse_key
        if self.delay_while_idle:
            json_dict['delay_while_idle'] = self.delay_while_idle
        if self.time_to_live:
            json_dict['time_to_live'] = self.time_to_live

        json_str = json.dumps(json_dict)
        return json_str


# Instantiate to send GCM message. No initialization required.
class GCMConnection:
    # Call this to send a push notification
    def notify_device(self, message):
        logging.warn("notify_device: %s" % str(message))
        # TODO: deal with memcache
        # self._incr_memcached(TOTAL_MESSAGES, 1)
        self._send_request(message)

    def delete_bad_token(self, bad_device_token):
        logging.info('delete_bad_token(): ' + repr(bad_device_token))

        # TODO: delete token in message

    def update_token(self, old_device_token, new_device_token):
        logging.info('update_token(): ' + repr((old_device_token, new_device_token)))

        # TODO: update token in message

    # Try sending message now
    def _send_request(self, message):
        if message.user == None or message.user.mobile_ids == None or message.notification == None:
            logging.error('Message must contain device_tokens and notification.')
            return False

        # Build request
        headers = { 'Authorization': 'key=' + carhubkeys.GCM_KEY, 'Content-Type': 'application/json' }

        gcm_post_json_str = ''
        try:
            gcm_post_json_str = message.json_string()
        except:
            logging.exception('Error generating json string for message: ' + repr(message))
            return

        logging.info('Sending gcm_post_body: ' + repr(gcm_post_json_str))

        request = urllib2.Request(GOOGLE_GCM_SEND_URL, gcm_post_json_str, headers)

        # Post
        try:
            resp = urllib2.urlopen(request)
            resp_json_str = resp.read()
            resp_json = json.loads(resp_json_str)
            logging.info('_send_request() resp_json: ' + repr(resp_json))

            failure = resp_json['failure']
            canonical_ids = resp_json['canonical_ids']
            results = resp_json['results']

            # If the value of failure and canonical_ids is 0, it's not necessary to parse the remainder of the response.
            if failure == 0 and canonical_ids == 0:
                # Success, nothing to do
                return
            else:
                # Process result messages for each token (result index matches original token index from message)
                result_index = 0
                for result in results:
                    if 'message_id' in result and 'registration_id' in result:
                        # Update device token
                        try:
                            old_device_token = message.device_tokens[result_index]
                            new_device_token = result['registration_id']
                            self.update_token(old_device_token, new_device_token)
                        except:
                            logging.exception('Error updating device token')
                        return

                    elif 'error' in result:
                        # Handle GCM error
                        error_msg = result.get('error')
                        try:
                            device_token = message.device_tokens[result_index]
                            self._on_error(device_token, error_msg, message)
                        except:
                            logging.exception('Error handling GCM error: ' + repr(error_msg))
                        return

                    result_index += 1

        except urllib2.HTTPError, e:
            # TODO: save errors...
            #self._incr_memcached(TOTAL_ERRORS, 1)

            if e.code == 400:
                logging.error('400, Invalid GCM JSON message: ' + repr(gcm_post_json_str))
            elif e.code == 401:
                logging.error('401, Error authenticating with GCM. Retrying message. Might need to fix auth key!')
            elif e.code == 500:
                logging.error('500, Internal error in the GCM server while trying to send message: ' + repr(gcm_post_json_str))
            elif e.code == 503:
                logging.error('503, Throttled. Retry after delay.')
            else:
                logging.exception('Unexpected HTTPError: ' + str(e.code) + " " + e.msg + " " + e.read())

    def _on_error(self, device_token, error_msg, message):
        # TODO: save errors...
        #self._incr_memcached(TOTAL_ERRORS, 1)

        if error_msg == "MissingRegistration":
            logging.error('ERROR: GCM message sent without device token. This should not happen!')

        elif error_msg == "InvalidRegistration":
            self.delete_bad_token(device_token)

        elif error_msg == "MismatchSenderId":
            logging.error('ERROR: Device token is tied to a different sender id: ' + repr(device_token))
            self.delete_bad_token(device_token)

        elif error_msg == "NotRegistered":
            self.delete_bad_token(device_token)

        elif error_msg == "MessageTooBig":
            logging.error("ERROR: GCM message too big (max 4096 bytes).")

        elif error_msg == "InvalidTtl":
            logging.error("ERROR: GCM Time to Live field must be an integer representing a duration in seconds between 0 and 2,419,200 (4 weeks).")

        elif error_msg == "MessageTooBig":
            logging.error("ERROR: GCM message too big (max 4096 bytes).")

        elif error_msg == "Unavailable":
            logging.error('ERROR: GCM Unavailable. Retry after delay.')

        elif error_msg == "InternalServerError":
            logging.error("ERROR: Internal error in the GCM server while trying to send message: " + repr(message))

        else:
            logging.error("Unknown error: %s for device token: %s" % (repr(error_msg), repr(device_token)))
