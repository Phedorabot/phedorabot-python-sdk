#!/usr/bin/env python
#
# Copyright 2017 Phedorabot
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import, division, print_function, with_statement

import json
import types
import hmac
import hashlib

class PhedorabotWebHookException(Exception):
    # The exception error
    def __init__(self, what, reason):
        self.what = what or None
        self.reason = reason or None

    def get_what(self):
        return self.what

    def get_reason(self):
        return self.reason


class PhedorabotWebHook(object):

    def __init__(self):
        # stuff goes here
        self.target_key = 'api_key'
        self.target_hmac_key = 'phedorabot_notification_digest'
        self.response = {}
        self.headers = {}
        self.checksum = None
        self.payload = {}
        self.apiKey = None
        self.apiSecret = None
        self.error = None
        self.errorDescription = None
        self.result = None
        self.body = None
        self.rawHeaderDict = {}

    def set_api_key(self, api_key):
        self.apiKey = api_key

    def get_api_key(self):
        return self.apiKey

    def set_raw_body(self, raw_body):
        self.body = raw_body or None

    def set_payload(self,payload):
        self.payload = payload or {}

    def get_payload(self):
        return self.payload

    def set_api_secret(self, secret):
        self.apiSecret = secret

    def get_api_secret(self):
        return self.apiSecret

    def set_raw_header(self, raw_header_dict):
        # Set the raw header that the server has so that we parse it to pick up
        # all Phedorabot related headers both the customer headers coming from
        # from Phedorabot
        self.rawHeaderDict = raw_header_dict or {}

    def _compute_hmac_string(self, attrs):
        # Flattern the attributes received from the notification server
        # you need to have set the apiKey and apiSecret before you can compute
        # the hmac of the data to verify the payload

        if self.apiSecret is None:
            raise PhedorabotWebHookException(
            'invalid_api_secret'
            , 'The corresponding api secret key is not defined for verifying \
            the integrity of this notification payload')

        flat = self._flatten_payload(attrs)
        sorted(flat)
        block = []
        for k in sorted(flat):
            block.append("{0}={1}".format(str(k), str(flat.get(k))))

        hasher = hmac.new(str(self.apiSecret), ''.join(block), hashlib.sha256)

        return str(hasher.hexdigest())

    def is_valid_notification(self):

        # first build the header dictionary and then locate the api key that
        # this notification is associated with
        # id for which this notification was generated. This is needed so we
        # could load from the database or some other storage the corresponding
        # secret key for verifying this notification payload
        is_valid = False
        try:
            self.will_validate_notification()
            # We should expect to find an api key from the notification
            # header with which we could verify the authenticity of the
            # payload
            if self.headers is None or \
            not self.headers.has_key(self.target_key):
                raise PhedorabotWebHookException(
                'invalid_api_key'
                , 'Notification does not include an api key')

            self.apiKey = str(self.headers.get(self.target_key))
            if not self.headers.has_key(self.target_hmac_key):
                raise PhedorabotWebHookException(
                'invalid_notification_digest'
                , 'Notification payload does not include a message digest '+
                'for verifying the notification payload')

            # At this point we set the validity to true to indicate that the
            # client can read the marketplace id and query their storage for
            # the corresponding secret key for further

            is_valid = True
        except (Exception, PhedorabotWebHookException) as ex:
            # raise an exeption to this effect
            if hasattr(ex, 'what'):
                # This is a custom exception
                self.error = ex.what
                self.errorDescription = ex.reason
            else:
                self.error = 'error'
                self.errorDescription = str(ex)
        finally:
            return is_valid

    def verify_payload(self):
        # If we do not have the body or the payload raise an exeption
        if not self.payload or not len(self.payload):
            raise PhedorabotWebHookException(
            'invalid_payload'
            , 'Notification has no body')

        # compute the hmac of the message and compare this computed hmac
        # with the one we found in the header payload, this will let us known
        # if the payload has been tempered with or not
        if not self.apiSecret or not len(self.apiSecret):
            raise PhedorabotWebHookException(
            'invalid_api_secret'
            , 'Notification engine parsing requires the corresponding '+
            'api secret key to verify the authenticity of the '+
            'notification payload')

        hmac_str = self._compute_hmac_string(self.payload)
        known_str = str(self.headers.get(self.target_hmac_key,''))
        print ('Known HMAC : {0}'.format(known_str))
        print ('Computed HMAC : {0}'.format(hmac_str))

        length = len(known_str) - 1
        i = 0
        validity = True
        self.checksum = 'verified'
        while(length > 0):
            delta = ord(known_str[i]) ^ ord(hmac_str[i])
            if delta:
                validity = False
                self.checksum = 'invalid'
                break
            else:
                i = i + 1
                length = length - 1

        return valid

    def will_validate_notification(self):

        self._build_headers()
        # parse the body of the message
        if self.body is None or not len(self.body):
            raise PhedorabotWebHookException(
            'invalid_notification_payload'
            , 'Notification payload is not defined')

        self.payload = json.loads(self.body)
        if not self.payload or not len(self.payload):
            raise PhedorabotWebHookException(
            'invalid_payload'
            , 'Notification pyaload could not be loaded')

        # Finally we need to ensure that the digest key is defined
        if not self.payload.has_key('digest_key'):
            raise PhedorabotWebHookException(
            'invalid_digest_key'
            , 'Notification payload does not define a valid digest key')

    def _flatten_payload(self, attrs, parent_key=None):
        # Flatten the payload so we could compute the hmac stringor message
        # digest to ensure that the payload has not been tempered with

        blobs = {}
        if attrs is None or not attrs in [types.DictType, types.ListType]:
            return blobs

        def value_type_check(value):
            # Checks a type and returns valid
            # string
            if type(value) == types.StringType:
                return str(value)
            elif type(value) == types.UnicodeType:
                value = value.encode('utf-8')
                return str(value)
            elif type(value) in [types.IntType, types.LongType]:
                return str(value)
            else:
                return str(value) if type(value) == types.NoneType else ''

        if type(attrs) == types.ListType:
            for i,val in enumerate(attrs):
                k = self._compute_valid_key(i, parent_key)
                if type(val) in [types.DictType,types.ListType]:
                    children = self._flatten_payload(val, k)
                    for m1,n1 in children.iteritems():
                        blobs[m1] = value_type_check(n1)
                else:
                    blobs[k] = value_type_check(val)

        if type(attrs) == types.DictType:
            for i,j in attrs.iteritems():
                k = self._compute_valie_key(i, parent_key)
                if type(j) in [types.DictType, types.ListType]:
                    children = self._flatten_payload(j, k)
                    for m1,n1 in children.iteritems():
                        blobs[m1] = value_type_check(n1)

        return blobs

    def _compute_valid_key(self, current_key, parent_key=None):
        if parent_key is not None:
            return '{0}_{1}'.format(str(current_key), str(parent_key))
        else:
            return str(current_key)

    def build_response(self):
        # builds a response that is sent to the notification server as
        # acknowledgement for the notification
        response = {}
        if self.checksum is None:
            response['checksum'] = 'unknown'
        else:
            response['checksum'] = self.checksum
        response['digest_key'] = self.payload.get('digest_key',None)

        return response

    def _build_headers(self):

        if type(self.rawHeaderDict) in [types.DictType, types.DictionaryType]:
            for k,v in self.rawHeaderDict.iteritems():
                k = str(k).lower()
                if k.startswith('x_'):
                    self.headers[k[2:]] = v
