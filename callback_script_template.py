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

# This is a script that shows how to handle the instant task execution post
# request from the Phedorabot server, you must ensure that this is done only
# with a post request

# import the webhook and the webhook excdeption class
from phedorabot.webhook import PhedorabotWebHookEngine
from phedorabot.webhook import PhedorabotWebHookException

# Wrap everything in a try/except block so we can deal with errors rightly

try:
    # First your server should be able to read the headers sent in as dictionary
    # and the raw body sent in
    # Initialize the webhook engine
    engine = PhedorabotWebHookEngine()
    # set the headers as a raw dictionary from your server
    engine.set_raw_header(server.request.headers)
    # set the raw boy as string type this will be parsed by the engine
    engine.set_raw_body(server.request.body)

    # Next we need to ensure that we received this instant task execution payload
    # from Phedorabot, before we can trust the payload enough to use it for
    # any meaningful task execution
    if engine.is_valid_task_execution():
        # Ok this looks good we have a valid task execution otherwise the webhook
        # will raise an exception for us
        # At this point we have a valid task execution payload we need to get
        # the public api key that is associated with this callback request data
        # so that you can provide the corresponding api secret for verifying the
        # integrity of the task payload
        api_key = engine.get_api_key()
        # Query for the corresponding api secret on your server, database or
        # configuration storage using this api key
        # after which set the below api secret to the corresponding secret

        api_secret = ''

        engine.set_api_secret(api_secret)
        # Next verify the integrity of the task execution payload
        if engine.verify_task_execution_payload():
            # Getting this far means that the tash execution payload is valid
            # and can be trusted.
            # get the headers incase you passed customer headers when creating
            # the task
            headers = engine.get_headers()
            # get the payload
            payload = engine.get_payload()

            # Now you can execute the task you want to execute here using the
            # contents of the payload as well as the headers after that if you
            # want to set customer status of the task execution you can call the
            # engine.add_result() method, this expects a key and a value
            # it will be registered on your Phedorabot task execution log so
            # you can review it later
            # e.g engine.add_result('status', 'Executed Successfully')
            # TODO: task executtion here, after this part you are all done
            # Note that Phedorabot server will give your server a 30 seconds
            # window to get feed back from this callback scripts otherwise it
            # will consider it a failure
            
except (Exception, PhedorabotWebHookException) as ex:
    # if this is a Phedorabot Webhook exception we need to capture it
    if hasattr(ex, 'what'):
        engine.set_error(ex.get_what())
        engine.set_error_description(ex.get_reason())
    else:
        engine.set_error('webhook_error')
        engine.set_error_description(str(ex))

finally:
    # send back response to Phedorabot so that you can see a log of how your
    # callback script is executing
    response = engine.get_response()
    # Print this depending on your server type
    print response
