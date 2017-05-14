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

# from phedorabot.api import PhedorabotAPIClient
# from phedorabot import exceptions

import json
import types
import hmac
import hashlib

def flatten_payload(attrs, parent_key=None):
    blobs = {}
    if attrs is None or not type(attrs) in [types.DictType, types.ListType]:
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
            k = compute_valid_key(i, parent_key)
            if type(val) in [types.DictType,types.ListType]:
                children = flatten_payload(val, k)
                for m1,n1 in children.iteritems():
                    blobs[m1] = value_type_check(n1)
            else:
                blobs[k] = value_type_check(val)

    if type(attrs) == types.DictType:
        for i,j in attrs.iteritems():
            k = compute_valid_key(i, parent_key)
            if type(j) in [types.DictType, types.ListType]:
                children = flatten_payload(j, k)
                for m1,n1 in children.iteritems():
                    blobs[m1] = value_type_check(n1)

    return blobs

def compute_valid_key(current_key, parent_key=None):
    if parent_key is not None:
        return '{0}_{1}'.format(str(current_key), str(parent_key))
    else:
        return str(current_key)


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


if __name__ == '__main__':

    maps = [{'name':'Christian','Age':'38'},{'name':'Vikky','age':'36'}]
    print(flatten_payload(maps))
