### Phedorabot Python Client SDK ###

Phedorabot is a task scheduling and cronjob APIs built for developers by
developers. Using Phedorabot makes it easier to delegate task execusion timing
and cronjobs to a third party service that is focus on triggering events when
their time is up.

Phedorabot uses callback URI to notify your server that a task is due for
execution and sends what is called **Instant Task Execution Notification**
as a **Post Request**, which comprises of custom fields and custom headers that
you provided when you scheduled a task on Phedorabot.

Phedorabot currently offers 4 services namely:

**Cronjob Service** is an API oriented time-based job scheduler that
anyone can use to schedule jobs that runs periodically at fixed times, dates or
intervals. It aims to make scheduling tasks very simple by exposing a simple
api for job scheduling. This service is most suitable for tasks that are
repititive in nature and spans an entire year or more.

Phedorabot Cronjob Service is similar to unix cron in nature only that you do not
have to be editing the crontab (cron table) file to setup shell commands that
should execute at a given time or date. The job configuration for unix cron and
Phedorabot Cronjob Service is the same, if you are familiar with configuring cron
on a unix system then you should be good with Phedorabot Cronjob Service. Please
note that Phedorabot Cronjob Service

**support only the standard cron configuration or scheduling macros**.
The following macros are not currently supported:

- @yearly or @annually
- @monthly
- @weekly
- @daily
- @hourly
- @reboot

A typical Phedorabot Cronjob schedule looks like this which is similar to
that of unix cron:

`
minute(0-59) hour(0-23) day-of-month(1-31) month(1-12) day-of-week(1-7)
`

To schedule a cronjob on Phedorabot, for example that runs twice a day, you can
use this cron configuration:

`
30 11,16 * * *
`

The above cron configuration will be interpreted as schedule a job that runs at
exactly 11:30 am and 4:30 pm every day of the week of every month.

- `30` 30th Minutes
- `11,16` 11 AM and 4 PM
- `*` Every day
- `*` Every month
- `*` Every day of the week

To learn more about Phedorabot Cronjobs refer to
[Cronjob API Documenation Guide](https://www.phedorabot.com/api/docs/#cron-task-schedule)

----------

**One Time Event Service** is an API oriented time-based job scheduler that
anyone can use to schedule jobs that runs exactly once at fixed times, dates
or intervals. It aims to make scheduling tasks very simple by exposing a simple
api for job scheduling. This service is most suitable for tasks that execute
exactly once in nature.

The one time event notification service allow clients to register events that
only executes once and after that are no longer valid for processing again,
although when such events execute and the client server is sent an instant
execution notification about the execution of the events, the client after
processing the event can still schedule a new one time event to be processed
at a later date.

This type of service is good for all types of reminders, For example if you want
to send a customer an email at a future date and you want your application to be
reminded of this, you can register an event with Phedorabot that should happen on
a future date and just forget about it, on the day that the event is due,
Phedorabot will send an instant execution notification to your application
registered callback uri with the details of the event which you provided
when you scheduled the event on Phedorabot.

This type of task is also suitable for student hostel reservation management
where you would want to deallocate a room after a given period of time from the
date the student reserved the room if the student has not already paid for the
room.

To schedule a one time job on Phedorabot, you need three important configuration
namely **time unit**(hour, day, week, month or year) and **period length** a
positive interger indicating duration and a contextual date from which the time
for the task to be executed will be computed. For contextual date, you can
specify a date string, acceptable date format on Phedorabot is **Y-m-d G:i:s**,
or you can specify a day in a month; a number between 1 and 31.

To learn more about Phedorabot One Time Event Service refer to
[One Time Event API Documenation Guide](https://www.phedorabot.com/api/docs/#onetime-task-schedule)

------------

**Recurrent Service** is an API oriented time-based job scheduler that anyone
can use to schedule jobs that runs recurrently at fixed times, dates or
intervals. It aims to make scheduling tasks very simple by exposing a simple
api for job scheduling. This service is most suitable for tasks that execute
recurrently at a given interval. This is different from Phedorabot cronjobs
because it does not build timepoint graphs but rather uses the configured time
unit and period length to compute the next execution date for the task.

The Recurrent Service allow clients to register events that recurrently execute
and automatically re-scheduled itself after it has executed when such event
executes, the client server is sent an instant execution notification with the
event details for further processing and Phedorabot server uses the configured
time unit and period length provided during the event scheduling with
Phedorabot to calculate the next time that the event is due for execution.

To learn more about Phedorabot Recurrent Service refer to
[Recurrent Service API Documenation Guide](https://www.phedorabot.com/api/docs/#recurrent-task-schedule)

-----------

To use the Python SDK, you should download or clone the phedorabot-python-sdk
to your server and then install the phedorabot package

`
cd phedorabot-python-sdk
sudo python setup.py install
`
After this phedorabot package will be available for use, to learn more how to
use, Phedorabot refer to the API Document for examples
