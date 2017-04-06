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

import requests
import json
import base64
from urlparse import urlparse
import time
import types
import jwt
from phedorabot.exceptions import PhedorabotAPIError
from phedorabot.response import PhedorabotAPIResponse

class PhedorabotAPIRequest(object):
    ''' This class encapsulate all request '''

    REQUEST_METHOD_POST = 'POST'
    REQUEST_METHOD_GET  = 'GET'
    JWT_EXPIRES         = 240

    def __init__(self):

        self.encode_data        = False
        self.authenticate       = False
        self.data               = None
        self.api_key            = None
        self.api_secret         = None
        self.base_uri           = None
        self.uri                = None
        self.headers            = {}
        self.response_headers   = {}
        self.access_token       = None
        self.access_token_type  = None
        self.debug              = False
        self._retry             = 3
        self._done              = False
        self._result            = None
        self.request_method     = self.REQUEST_METHOD_POST

    def with_encode_data(self):
        self.encode_data = True

    def with_authentication(self):
        self.authenticate = True

    def set_base_uri(self, uri):
        self.base_uri = uri

    def set_uri(self, uri):
        self.uri = uri

    def set_access_token(self, token):
        self.access_token = token

    def set_access_token_type(self, token_type):
        self.access_token_type = token_type

    def set_api_key(self, apikey):
        self.api_key = apikey

    def set_api_secret(self, apisecret):
        self.api_secret = apisecret

    def add_header(self, hkey, hvalue):
        self.headers[str(hkey)] = str(hvalue)

    def add_headers(self, headers):
        for key, value in headers.iteritems():
            self.add_header(key, value)

    def set_data(self, data):
        self.data = data

    def with_debug(self):
        self.debug = True

    def set_request_method(self, method):

        known_methods = {
        self.REQUEST_METHOD_POST : 1,
        self.REQUEST_METHOD_GET : 1,
        }

        if method is not None:
            method = method.upper()
            if not known_methods.has_key(method):
                raise PhedorabotAPIError(
                'invalid_request_method'
                , 'Method '+method+' is not a valid API request method')

            self.request_method = method

    def make_basic_auth_string(self, api_key, api_secret):

        if api_key is None or api_secret is None:
            raise PhedorabotAPIError(
            'invalid_api_keys'
            , 'Building Basic Authentication requires authentication '+
            'parameters')

        attrs = '{0}:{1}'.format(api_key, api_secret)
        attrs = attrs.encode('latin1').strip().decode('latin1')
        return 'Basic '+base64.b64encode(attrs)

    def _decode_response(self,response):

        # use pyjwt to decode the response
        if response is None or not len(response):
            raise PhedorabotAPIError(
            'invalid_payload'
            , 'Expected a JWT string to be decoded none given')

        if self.api_secret is None:
            raise PhedorabotAPIError(
            'invalid_api_keys'
            , 'Decoding a JWT encoded payload requires the transaction '+
            'api id and secret key')

        try:

            output = jwt.decode(response, self.api_secret)
            header = jwt.get_unverified_header(response)

            header = self._verify_response_data(header, 'Header')
            output = self._verify_response_data(output, 'Payload')

            if str(header.get('iss')) != 'PhedorabotAPI':
                raise ValueError(
                'Received an invalid issuer identification from api server')

            if str(header.get('aud')) != str(self.api_key):
                raise ValueError(
                'Received an invalid audience identification from the '+
                'api server')

            self.response_headers = header
            return output

        except (jwt.DecodeError, ValueError) as e:
            raise PhedorabotAPIError('invalid_jwt_payload' ,str(e))

    def _parse_response(self, raw_response):

        if raw_response is None or not len(raw_response):
            raise PhedorabotAPIError(
            "invalid_response"
            , "Received an invalid response from the server")

        try:

            response = json.loads(raw_response)
            if type(response) not \
            in [types.DictionaryType, types.DictType]:
                raise PhedorabotAPIError(
                "invalid_response"
                , "Received response could not be decoded to JSON object")

            if response.has_key('jwt'):
                response = self._decode_response(response['jwt'])

            if type(response) == types.DictType:
                if response.has_key('error'):
                    raise PhedorabotAPIError(
                    response.get('error')
                    , response.get('error_description'))

                if response.has_key('result'):
                    return response.get('result')
                return response
            else:
                return response

        except Exception as e:
            if hasattr(e,'what'):
                raise e
            else:
                raise PhedorabotAPIError('invalid_response',str(e))

    def _verify_response_data(self, data, data_type):

        if not data or type(data) not in [types.DictType, types.ListType]:
            msg = 'Received an invalid {0} data'.format(data_type)
            raise PhedorabotAPIError('invalid_data', msg)
        return data

    def make_api_call(self):

        data = self.data
        if data is not None:
            if self.encode_data:
                if not self.api_key or not self.api_secret:
                    raise PhedorabotAPIError(
                    'invalid_marketplace_keys'
                    , 'This request requires that the data payload be JWT '+
                    'encoded but the marketplace id and secret needed to JWT '+
                    'encode the data are not defined')

                if not self.api_key or not self.api_secret:
                    raise PhedorabotAPIError(
                    'invalid_api_keys'
                    , 'This request requires that the data payload be JWT '+
                    'encoded but the required api key and secret are not '+
                    'defined')

                headers = {}
                headers['aud'] = 'PhedorabotAPI'
                headers['iss'] = str(self.api_key)
                headers['iat'] = int(time.time())
                headers['exp'] = int(time.time()) + self.JWT_EXPIRES

                data = jwt.encode(
                data
                , self.api_secret
                , 'HS256'
                , headers)

                data = {'jwt':data}
                self.add_header('X-Phedorabot-Api-Key', self.api_key)

        if self.authenticate:
            # perform authentication request here
            if self.api_key is None or self.api_secret is None:
                raise PhedorabotAPIError(
                'invalid_api_keys'
                , 'Phedorabot API authentication requires your api key and '+
                'secret')

            self.add_header('Accept','application/json')
            self.add_header('Accept-Language','en_US')
            self.add_header(
            'Authorization'
            , self.make_basic_auth_string(self.api_key, self.api_secret))

        else:
            # we are sending out data tothe server
            self.add_header('Content-Type', 'application/json')
            self.add_header(
            'Authorization'
            , '{0} {1}'.format(self.access_token_type, self.access_token))

        if self.base_uri is None or not len(self.base_uri):
            raise PhedorabotAPIError(
            'invalid_base_uri'
            , ' This request does not define a base request uri')

        if self.uri is None or not len(self.uri):
            raise PhedorabotAPIError(
            'invalid_request_uri'
            , 'This request does not defined a transaction uri')

        # Get a connection
        error = None
        while self._retry > 0:

            if self._done:
                break
            try:
                self._try_request(data, self.base_uri, self.uri)
            except Exception as ex:
                self._retry -= 1
                error = str(ex)

        if error is not None:
            return PhedorabotAPIResponse(None, error, self.response_headers)

        # We should have a result
        if self._result is None or not len(self._result):
            return PhedorabotAPIResponse(
            None
            , 'Invalid response from API Server'
            , self.response_headers)

        try:
            body = self._parse_response(self._result)
            return PhedorabotAPIResponse(body, None, self.response_headers)

        except PhedorabotAPIError as ex:
            return PhedorabotAPIResponse(None, str(ex), self.response_headers)

    def _try_request(self, data, base_uri, uri):
        # using the installed requests module
        if data is None:
            data = {}

        try:
            # build the destination uri from the base uri and the target
            # uri
            if not base_uri.endswith('/'):
                base_uri = base_uri+'/'

            if uri.startswith('/'):
                uri = uri[1:]

            if not uri.endswith('/'):
                uri = uri+'/'

            path = '{0}{1}'.format(base_uri, uri)
            r = requests.post(path, data=data, headers=self.headers)

            if self.debug:
                # print the debug message
                print ('Request Path :'+path)
                print ('Response status code : '+r.status_code)
                print ('Response Headers :', r.headers)


            if r.status_code != 200:
                if r.text is not None and len(r.text):
                    self._result = str(r.text)
                else:
                    raise Exception('Invalid API server response')

            else:
                self._result = str(r.text)

            self._done = True

        except Exception as ex:
            self._done = True
            raise ex
