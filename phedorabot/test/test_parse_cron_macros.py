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

import phedorabot
from phedorabot.exceptions import PhedorabotAPIError
from phedorabot.test.config import Config
from phedorabot.cronjob import PhedorabotCronjobSchedulerAPIClient

if __name__ == '__main__':

    # Get a client, force the client to request for a fresh access token
    client = phedorabot.PhedorabotClient(Config.api_key, Config.api_secret)

    # Get a list object
    cron = PhedorabotCronjobSchedulerAPIClient()
    cron.set_subscription_id('crj_124016002236127285')
    cron.set_cron_macros('30 11 * * *')
    cron.set_request_uri('/cron/script/parse')

    try:
        resp = client.request.send(cron)

        if resp.is_failure():
            # We have an error
            raise PhedorabotAPIError('error', resp.get_error())
        print (resp.get_raw_data())

    except(PhedorabotAPIError) as e:
        print(e)
