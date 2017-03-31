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

"""The Phedorabot Python SDK."""

from __future__ import absolute_import, division, print_function, with_statement

# version is a human-readable version number.

# version_info is a four-tuple for programmatic comparison. The first
# three numbers are the components of the version number.  The fourth
# is zero for an official release, positive for a development branch,
# or negative for a release candidate or beta (after the base version
# number has been incremented)

version = "1.0.0"
version_info = (1, 0, 0, -100)

def memoize(f):
    """
    Memoization decorator
    """
    cache= {}
    def func(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return func

class PhedorabotClient(object):

    def __init__(self, api_key, api_secret, access_token=None):

        self.api_key = api_key or None
        self.api_secret = api_secret or None
        self.options = {}

        if access_token is not None:
            self.options['access_token'] = str(access_token)
            self.options['access_token_type'] = 'Bearer'

    @property
    @memoize
    def request(self):

        from phedorabot import web
        return web.Http(self.api_key, self.api_secret, **self.options)

    def request_rate_limit(self, api_key, api_secret):
        from phedorabot import web
        return web.Http.request_rate_limit(api_key,api_secret)
