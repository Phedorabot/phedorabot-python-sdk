from phedorabot.webhook import PhedorabotWebHookEngine
from phedorabot.webhook import PhedorabotWebHookException
import json
import sys

data_template="""
{"cronjob_id":"295039090705787663",
  "service_name":"Recurrent Event Service",
  "subscription_id":"rcu_353431617358994734",
  "execution_id":"274295575708856625",
  "task_name":"Recurrent event for 2017-03-21 8:18:22",
  "execution_epoch":"1492759102",
  "execution_date":"April 21st, 2017 at 7:18 am",
  "next_epoch":"1495351102",
  "next_execution_date":"May 21st, 2017 at 7:18 am",
  "cronjob_script":null,
  "properties":{"random.key":"er6ttejgsmtx"}
}
"""

data_template="""
{"job_id":"352667059500430128","service_name":"One Time Trigger Service","subscription_id":"ott_110801827011331707","execution_id":"166887952632453844","task_name":"RAJI TARIQ","execution_epoch":"1514446200","execution_date":"December 28th, 2017 at 7:30 am","next_epoch":"1545982200","next_execution_date":"December 28th, 2018 at 7:30 am","task_duration":"1 Year","user_guid":"6lmhcmazsltepsxwtyrt","user_birthday_epoch":"1514446200","family_guids":"xfl3neemltidwc3xirvo,f5dvlspdldlfsmlnfqop\r\n"}
"""
header_template="""
{
  "X_PHEDORABOT_NOTIFICATION_DIGEST":"965d207a58a302562a548fa28fcdc0611343d8b0f8664c2ccf918f2f80497fa4",
  "X_PHEDORABOT_SENT_THIS":"1",
  "X_PHEDORABOT_API_KEY":"YlNiZQp0QWlkVnBJQ0g4"
}
"""

if __name__ == '__main__':

    # Wrap in a try catch block
    engine = PhedorabotWebHookEngine()
    # Set the raw headers, this hsould normally be gotten from you web server
    #
    engine.set_raw_header(json.loads(header_template))
    # set the post body
    engine.set_raw_body(data_template)

    try:
        # if we could not verify the payload coming from Phedorabot server
        # we have a problem
        if engine.is_valid_task_execution():
            # We have a valid payload coming from Phedorabot server we now need
            # verify the payload to ensure that it has not been tempered with
            # on its way to your server
            # The api key would have been extracted from the headers coming and
            # parsed in the check above so we need to get access to it so that
            # we can select the right corresponding private key
            api_key = engine.get_api_key()
            if not api_key or not len(api_key):
                raise PhedorabotWebHookException(
                'invalid_api_key'
                , 'Client api key is not defined in the header payload for \
                this task execution')

            # At this point query fro the corresponding private key related to
            # this public key
            secret_key = 'SFUraUVjU2RUeDRoemNXTnJaaXVEZGJNRW9TRFN5'
            # Now set the secret key, so we could verify the payload data
            engine.set_api_secret(secret_key)
            # Try to verify the payload
            if not engine.verify_task_execution_payload():
                # The payload could not be verified
                raise PhedorabotWebHookException(
                'payload_checksum_error'
                , 'Payload checksum failed data integrity test')
            # We have a valid payload which we can now extract for process
            data = engine.get_payload()
            headers = engine.get_headers()
            # use the data to runn the job you wanted to run, ensure that
            # you do not waste time here so that you can send back response
            # to Phedorabot but server on the status of this execution
            # TODO: run you tasks based on the data provided here
            print 'Task running...'
            print (headers)
    except (Exception, PhedorabotWebHookException) as ex:
        # This is to ensure that we capture this error on the task execution
        # log
        if hasattr(ex, 'what'):
            engine.set_error(ex.get_what())
            engine.set_error_description(ex.get_reason())
        else:
            engine.set_error('error')
            engine.set_error_description(str(ex))

    finally:
        # Ensure that you update Phedorabot server with the status of the
        # instant task execution, so that you can get the log messages for your
        # task executions
        response = engine.get_response()
        # send the response back to Phedorabot server for logs by printing
        # the json encoded version of the response
        print (json.dumps(response))
