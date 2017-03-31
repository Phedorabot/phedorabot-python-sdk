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
'PhedorabotRecurrentSchedulerAPIClient')

'''A Phedorabot Recurrent Scheduler API Client Library.

For full API documentation, visit https://www.phedorabot.com/api/docs/.

Typical usage:

    client = phedorabot.PhedorabotClient(
    api_key=..., api_secret=..., access_token=...)
    recurrent = PhedorabotRecurrentSchedulerAPIClient()
    resp = client.request.send(recurrent)
    if resp.is_error():
        print response.get_error()
    else:
        data = resp.get_raw_data()
'''


class PhedorabotRecurrentSchedulerAPIClient(PhedorabotAPIClient):
    ''' Schedule recurrent tasks on Phedorabot for executions'''

    def __init__(self):

        super(PhedorabotRecurrentSchedulerAPIClient, self).__init__()
        self.parameters = None
        self.set_starting_at(0)
        self.set_paging_limit(100)

    def set_subscription_id(self, sid):
        ''' Subscription ID

        Set the recurrent subscription id as shown on your Phedorabot Recurrent
        subscription page
        '''
        if sid is not None:
            self.set_parameter('subscription_id', str(sid))

    def set_job_id(self, jid):
        ''' Set the Job ID of the cronjob task '''
        if jid is not None:
         self.set_parameter('job_id', jid)

    def set_task_name(self, task_name):
        ''' Task Name

        Set the recurrent task to be used for identifying the task, not more
        than 64 characters
        '''
        if task_name is not None:
            self.set_parameter('task_name', str(task_name))

    def set_task_description(self, task_description):
        ''' Task Description

        Set the recurrent task description to be used for explaining what the
        task is doing, not more than 160 characters
        '''

        if task_description is not None:
            self.set_parameter('task_description', str(task_description))

    def add_custom_property(self, prop_key, prop_value):
        ''' Add Custom Properties
        This will be returned along with the Instant Execution Notification
        payload that will be sent to you
        '''
        if prop_key is not None and prop_value is not None:
            props = self.get_parameter('recurrent_properties', {})
            props[str(prop_key)] = prop_value
            self.set_parameter('recurrent_properties', props)

    def add_custom_header(self, head_key, head_value):
        ''' Custom Headers
        This will be added to the header of the Instant Execution Notification
        payload that will be sent to your server
        '''

        if head_key is not None and head_value is not None:
            headers = self.get_parameter('recurrent_headers', {})
            headers[str(head_key)] = head_value
            self.set_parameter('recurrent_headers', props)

    def set_time_unit(self, time_unit):
        ''' Time Unit

        Time unit is part of what make up the duration of the task or how long
        it will take for the task to executed, valid time units are
        (hour, day, week, month or year) for example if you want to execute a
        task in 2 weeks time then the time unit will be 'week'
        '''
        valid_time_units = {'hour':1,'day':1,'week':1,'month':1,'year':1}

        if not time_unit or not len(time_unit):
            raise exceptions.PhedorabotAPIError(
            'invalid_time_unit'
            , 'Time unit '+time_unit+' is not valid')

        if not valid_time_units.has_key(time_unit):
            raise exceptions.PhedorabotAPIError(
            'invalid_time_unit'
            , 'Provided time unit '+time_unit+' is not a valid time unit')

        self.set_parameter('time_unit', time_unit)

    def set_period_length(self, period_length):
        ''' Period Length
        Period length is part of what makes up the duration of the task or how
        long it will take for the task to be executed, valid period length are
        positive numbers. For example if you want a task to be executed 1 month
        from today, then the period length is 1 and the time unit is month
        '''
        try:
            period_length = int(period_length)
        except Exception as e:
            raise exceptions.PhedorabotAPIError(
            'invalid_period_length'
            , 'Period length is not valid {0}'.format(str(e)))

        self.set_parameter('period_length', period_length)

    def set_start_date(self, start_date):
        ''' Start Date
        This is the contextual date that should be used for calculating when
        this task will execute for the first time, acceptable dates is of the
        format 'Year-Month-Day Hour:Minutes:seconds' for example
        '2017-06-14 10:30:00' is a valid date, which means for example if you
        set time_unit to be 'month' and period_length to be '1' then this task
        will be executed on the 14th of July 2017 at 10:30 am
        '''

        parts = start_date.split(' ')
        if len(parts) != 2:
            raise exceptions.PhedorabotAPIError(
            'invalid_start_date'
            , 'Start date should consist of both the date and the time')

        date_parts = parts[0].split('-')
        time_parts = parts[1].split(':')

        if len(date_parts) != 3:
            raise exceptions.PhedorabotAPIError(
            'invalid_start_date'
            , 'The date portion of the start date is not valid')

        if len(time_parts) != 3:
            raise exceptions.PhedorabotAPIError(
            'invalid_start_date'
            , 'The time portion of the start date is not valid')

        self.set_parameter('start_date', start_date)

    def set_day_of_month(self, day):
        ''' Day of month
        Day of the month is a number between 1 to 31, this number means
        that you want Phedorabot to use the day of the month as the contextual
        date for calculating when the task should start executing.

        For example, if today is February 15 and you set this day to be 14,
        then the contextual date will be set to 14th of March. If you set the
        day to be 18, then the contextual date will be set to February 18th;
        if you set the day to be 15, then the contextual date will be set to
        today, using this contextual date we can then compute when the
        task should start executing.

        If you want the contextual date to be at the end of the month
        regardless of the month, then set the day to 31
        '''
        valid_ranges = range(1, 32)

        try:
            day = int(day)
            if not day in valid_ranges:
                raise Exception('Day of month {0} is not valid'.format(day))
        except Exception as e:
            raise exceptions.PhedorabotAPIError('invalid_day_of_month', str(e))

        self.set_parameter('day_of_month', day)

    def should_start_immediately(self):
        ''' Start Immediately

        If you do not want to set a start date or a day of the month you can
        call this method, it will tell Phedorabot to use the current date and
        time at which you request was recieved by the api to calculate when
        the task will be executed
        '''
        self.set_parameter('start_immediately', true)

    def with_exclude_weekends(self):
        ''' Exclude Weekends (Sartuday and Sundays)

        With the given contextual date from which to calculate when the task
        will be executed, if this option is set, Phedorabot will calculate the
        normal task execute date from this, then it will scan through to remove
        all Sartudays and Sundays, the implication is that execution date will
        be pushed forward by some days depending on how many weekends where
        found
        '''
        self.set_parameter('exclude_weekends', true)

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
