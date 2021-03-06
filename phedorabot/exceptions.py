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

class PhedorabotAPIError(Exception):
    ''' The Phedorabot Python SDK exception class '''

    def __init__(self, what, reason):
        self.what = what or ''
        self.reason = reason or ''

    def __str__(self):
        return "Error <{0}:{1}>".format(self.what, self.reason)

    def get_what(self):
        return self.what

    def get_reason(self):
        return self.reason
