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
'PhedorabotSMSSchedulerAPIClient')

'''A Phedorabot SMS Transactional Message Scheduler API Client Library.

For full API documentation, visit https://www.phedorabot.com/api/docs/.

Typical usage:

    client = phedorabot.PhedorabotClient(
    api_key=..., api_secret=..., access_token=...)
    sms = PhedorabotSMSSchedulerAPIClient()
    sms.add_recipient('number','message')
    resp = client.request.send(sms)
    if resp.is_error():
        print response.get_error()
    else:
        data = resp.get_raw_data()
'''


class PhedorabotSMSSchedulerAPIClient(PhedorabotAPIClient):
    ''' Schedule a transactional sms message on Phedorabot for executions'''

    def __init__(self):
        super(PhedorabotSMSSchedulerAPIClient, self).__init__()
        self.parameters = None
        self.set_starting_at(0)
        self.set_paging_limit(100)

    def set_subscription_id(self, sid):
        ''' Subscription ID

        Set the one time subscription id as shown on your Phedorabot SMS page
        '''
        if sid is not None:
            self.set_parameter('subscription_id', str(sid))

    def set_job_id(self, jid):
        ''' Set the Job ID of the sms task '''
        if jid is not None:
         self.set_parameter('job_id', jid)

    def set_task_name(self, task_name):
        ''' Task Name

        Set the sms task to be used for identifying the task, not more than
        64 characters
        '''
        if task_name is not None:
            self.set_parameter('task_name', str(task_name))

    def set_task_description(self, task_description):
        ''' Task Description

        Set the sms task description to be used for explaining what the
        tast is doing, not more than 160 characters
        '''
        if task_description is not None:
            self.set_parameter('task_description', str(task_description))

    def add_custom_property(self, prop_key, prop_value):
        ''' Add Custom Properties
        This will be returned along with the Instant Execution Notification
        payload that will be sent to you
        '''
        if prop_key is not None and prop_value is not None:
            props = self.get_parameter('sms_properties', {})
            props[str(prop_key)] = prop_value
            self.set_parameter('sms_properties', props)

    def add_custom_header(self, head_key, head_value):
        ''' Custom Headers
        This will be added to the header of the Instant Execution Notification
        payload that will be sent to your server
        '''

        if head_key is not None and head_value is not None:
            headers = self.get_parameter('sms_headers', {})
            headers[str(head_key)] = head_value
            self.set_parameter('sms_headers', props)

    def add_recipient(
    self, standard_number, body, time_unit=None, period_length=None):
        ''' Add Recipient
        Adding a new SMS recipient requires proving the following

        - standard_number: (required) the mobile number of the recipient with
                           the country code attached to it example +234807676565.

        - message : (required) The message that should be sent to this
                    recipient messages are normally not more than 160
                    characters, however the more characters you have the more
                    pages will be generated for delivery the sms to the client
                    and the more sms credit that will be used.

        - time_unit : (optional) This is provided when you want the sms to be
                 delivered at a future time. Its usually one of
                 (minute, hour, day, week). Example if you want an sms to be
                 delivered to your client say three days from today, you need
                 to set the time_unit to 'day' and the period_length to '3'

        - period_length : (optional) This is provided when you want the sms to
                          be delivered at a future time. Its usually a
                          positive number. Example of you want an sms
                          delivered to be delivered to your client in 2 weeks
                          time, you would set the time_unit to 'week' and
                          the period_length to  '2'

        '''

        recipients = self.get_parameter('recipients', [])
        if standard_number and len(standard_number) and body and len(body):
            recipients.append(dict(
            number=standard_number,
            body=body,
            time_unit=time_unit,
            period_length=period_length
            ))

            self.set_parameter('recipients', recipients)


    def set_sender_id(self, sender_id):
        ''' Sender ID

        The sender id is a short string that can be used to identify the
        service, company or individual that is sending the message, this most
        be at most 11 characters in length
        '''
        if sender_id and len(sender_id):
            self.set_parameter('sender_id', str(sender_id))

    def set_callback_uri(self, uri):
        ''' Callback uri

       The callback uri is a fully qualified url for receiving
       Instant Execution Notification (IEN)
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
