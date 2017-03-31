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

from phedorabot.exceptions import PhedorabotAPIError

class PhedorabotAPIClient(object):

    def __init__(self):

        self.uri         = None
        self.parameters  = {}
        self.api_key     = None
        self.api_secret  = None
        self.debug       = False

    def set_request_uri(self, uri):
        self.uri = uri

    def get_request_uri(self):
        if not len(self.uri) or self.uri is None:
            raise PhedorabotAPIError(
            'invalid_request_uri', 'Request uri is not defined')

        return self.uri
    def require_api_keypair(self):

        if self.api_key is None or self.api_secret is None:
            raise PhedorabotAPIError(
            'invalid_api_keys'
            , 'Api key and Secret key are required for to initiate a '+
            'communication with the Phedorabot API')

    def set_parameter(self, key, value):
        if self.parameters is None:
            self.parameters = dict()

        if key and not self.parameters.has_key(str(key)):
            self.parameters[str(key)] = value

    def get_parameter(self, key, default=None):

        if self.parameters is None:
            return default
        else:
            return self.parameters.get(str(key), default)

    def set_api_key(self, api_key):
        self.api_key = api_key

    def get_api_key(self):
        return self.api_key or None

    def set_api_secret(self, api_secret):
        self.api_secret = api_secret

    def get_api_secret(self):
        return self.api_secret or None

    def set_starting_at(self, at):
        self.set_parameter('starting_at', at)

    def set_paging_limit(self, lm):
        self.set_parameter('limit', lm)

    def build_request_dictionary(self):

        if self.api_key is not None:
            pass
        return self.parameters if self.parameters else {}

    def __str__(self):
        attrs = {}
        for k, v in self.__dict__.iteritems():
            attrs[k] = v
        import json
        return json.dumps(attrs)
