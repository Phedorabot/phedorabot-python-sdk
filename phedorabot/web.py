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

from phedorabot import exceptions
from phedorabot.api import PhedorabotAPIClient
from phedorabot.request import PhedorabotAPIRequest

try:
    import json
except ImportError:
    import simplejson as json

class Http(object):

    END_POINT = 'https://www.phedorabot.com/api/v1/'
    JWT_EXPIRES       = 240

    def __init__(self, api_key, api_secret, **options):

        self.api_key            = api_key
        self.api_secret         = api_secret
        self.call_type          = None
        self.access_token       = options.get('access_token', None)
        self.token_type         = options.get('access_token_type', None)
        self.debug              = options.get('debug', False)

    def require_access_token(self):

        if self.access_token is None:
            data = {'grant_type':'client_credentials',}

            req = PhedorabotAPIRequest()
            req.set_data(data)
            req.set_uri('/authentication/client/accesstoken/')
            req.set_api_key(self.api_key)
            req.set_api_secret(self.api_secret)
            req.set_request_method('POST')
            req.set_base_uri(self.END_POINT)

            if self.debug:
                req.with_debug()

            req.with_authentication()
            response = req.make_api_call()

            if response.is_error():
                raise exceptions.PhedorabotAPIError(
                'invalid_response'
                , response.get_error())

            self.access_token = response.get_body().get('access_token')
            self.token_type = response.get_body().get('access_token_type')


    def require_api_keypair(self):

        if self.api_key is None or self.api_secret is None:
            raise exceptions.PhedorabotAPIError(
            'invalid_api_key'
            , 'API ID and Secret key are required for this request')

        if len(self.api_key) < 10 or len(self.api_secret) < 10:
            raise exceptions.PhedorabotAPIError(
            'invalid_api_key'
            , 'Provide your valid api key')

    def fetch(self, request):
        return self.send(request, True)

    def send(self, request, need_token=True):

        self.require_api_keypair()
        self.debug = request.debug

        if need_token:
            self.require_access_token()
            if self.access_token is None or self.token_type is None:
                raise exceptions.PhedorabotAPIError(
                'invalid_access_token'
                , 'Requesting instant transaction access token from the '+
                'or server failed')

        # request.require_api_keypair()

        if request.get_request_uri() is None:
            raise exceptions.PhedorabotAPIError(
            'invalid_request_path'
            , 'Request path is not specified for this transaction')

        request_uri = None
        base_uri = Http.END_POINT
        uri = request.get_request_uri()

        data = request.build_request_dictionary()

        req = PhedorabotAPIRequest()
        req.set_base_uri(base_uri)
        req.set_uri(uri)
        req.set_api_key(self.api_key)
        req.set_api_secret(self.api_secret)
        req.set_access_token(self.access_token)
        req.set_access_token_type(self.token_type)
        req.set_data(data)
        req.set_request_method('POST')
        if self.debug:
            req.with_debug()

        req.with_encode_data()
        response = req.make_api_call()
        return response

    @staticmethod
    def request_rate_limit(api_key, api_secret):
        # request your current rate limit without encuring
        # rate limit application
        if api_key is None or api_secret is None:
            raise exceptions.PhedorabotAPIError(
            'invalid_api_keys'
            , 'Requesting for your rate limit requires your API Key and Secret')

        request = Http(api_key ,api_secret)
        data = {}
        req = PhedorabotAPIRequest()
        req.set_api_key(api_key)
        req.set_api_secret(api_secret)
        req.set_data(data)
        req.set_uri('/ratelimit/')
        req.set_base_uri(Http.LIVE_END_POINT)
        req.with_authentication()
        response = req.make_api_call()
        return response
