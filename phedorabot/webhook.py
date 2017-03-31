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

from phedorabot.api import PhedorabotAPIClient
from phedorabot import exceptions

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
