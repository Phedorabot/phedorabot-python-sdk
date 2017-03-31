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
import types

class PhedorabotAPIResponse(object):

    def __init__(self, body, error=None, headers=None):

        self.error = error
        self.headers = headers
        self.has_more = False
        self.data = []
        self.starting_at = 0
        self.limit = 100
        self.body = self._parse_body(body)


    def is_success(self):
        if self.error is not None:
            return False
        else:
            return True

    def is_failure(self):
        if self.error is not None:
            return True
        else:
            return False

    def is_error(self):
        return self.is_failure()

    def get_headers(self):
        return self.headers

    def get_data(self):
        return self.data

    def get_raw_data(self):
        return self.get_body()

    def get_body(self):
        return self.body

    def get_error(self):
        return self.error

    def _parse_body(self,body):

        if body is not None:
            raw_body = body.copy()
            if type(raw_body) == types.DictType:
                if raw_body.has_key(u'data'):
                    self.starting_at = raw_body['starting_at']
                    self.data = raw_body['data']
                    self.has_more = bool(raw_body['has_more'])
        return body
