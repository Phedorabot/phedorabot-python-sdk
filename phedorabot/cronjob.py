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

__all__ = (
'PhedorabotCronjobSchedulerAPIClient')

'''A Phedorabot Cronjob Scheduler API Client Library.

For full API documentation, visit https://www.phedorabot.com/api/docs/.

Typical usage:

    client = phedorabot.PhedorabotClient(
    api_key=..., api_secret=..., access_token=...)
    cron = PhedorabotCronjobSchedulerAPIClient()
    resp = client.request.send(cron)
    if resp.is_error():
        print response.get_error()
    else:
        data = resp.get_raw_data()
'''


class PhedorabotCronjobSchedulerAPIClient(PhedorabotAPIClient):
    ''' Schedule cronjobs on Phedorabot for executions'''

    def __init__(self):
        super(PhedorabotCronjobSchedulerAPIClient, self).__init__()
        self.parameters = None
        self.set_starting_at(0)
        self.set_paging_limit(100)

    def set_job_id(self, jid):
        ''' Set the Job ID of the cronjob task '''
        if jid is not None:
         self.set_parameter('job_id', jid)

    def set_subscription_id(self, sid):
        ''' Subscription ID

        Set the cronjob subscription id is shown on your Phedorabot cronjob
        subscription page
        '''
        if sid is not None:
            self.set_parameter('subscription_id', str(sid))

    def set_task_name(self, task_name):
        ''' Task Name

        Set the cronjob task to be used for identifying the task, not more than
        64 characters
        '''
        if task_name is not None:
            self.set_parameter('task_name', str(task_name))

    def set_cron_macros(self, macros):
        ''' Cron Macros

        The cronjob script that needs to be parsed to build the cronjob time
        point graph
        '''
        if macros is not None and len(macros):
            self.set_parameter('cron_script', macros)

    def set_task_description(self, task_description):
        ''' Task Description

        Set the cronjob task description to be used for explaining what the task
        is doing, not more than 160 characters
        '''
        if task_description is not None:
            self.set_parameter('task_description', str(task_description))

    def add_custom_property(self, prop_key, prop_value):
        ''' Add Custom Properties
        '''
        if prop_key is not None and prop_value is not None:
            props = self.get_parameter('cron_properties', {})
            props[str(prop_key)] = prop_value
            self.set_parameter('cron_properties', props)

    def add_custom_header(self, head_key, head_value):
        ''' Custom Headers
        '''

        if head_key is not None and head_value is not None:
            headers = self.get_parameter('cron_headers', {})
            headers[str(head_key)] = head_value
            self.set_parameter('cron_headers', props)


    def set_callback_uri(self, uri):
        ''' Cronjob callback uri

       The callback uri is a fully qualified url for receiving
       Instant Execution Notification (IEN) describing what has

       An example listener is something like this:
       http://website.com/task/execution_listener.php
       this url will always receive a POST from Phedorabot
       '''
        if uri is not None:
            if len(str(uri)) >= 2087:
                raise exceptions.PhedorabotAPIError(
                'invalid_callback_uri'
                , 'Callback uri is not valid must be a valid uri and \
                not more than 2087 characters in length')
            self.set_parameter('callback_uri', str(uri))
