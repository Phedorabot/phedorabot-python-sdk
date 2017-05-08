from phedorabot.webhook import PhedorabotWebHook
from phedorabot.webhook import PhedorabotWebHookException
import json
import sys

template ="""
{"headers":{"phedorabot_sent_this":"true"
,"phedorabot_api_key":"1902989276275"
,"phedorabot_notification_digest":"d15a2c87425699d43b68d8c33ea1eaf052aa1fde94fae14711b5f27f9f617d62"}
,"raw_headers":{
"X_PHEDORABOT_SENT_THIS":"true"
,"X_PHEDORABOT_API_KEY":"1902989276275"
,"X_PHEDORABOT_NOTIFICATION_DIGEST":"d15a2c87425699d43b68d8c33ea1eaf052aa1fde94fae14711b5f27f9f617d62"
,"REQUEST_TIME_FLOAT":1435767624.074
,"REQUEST_TIME":1435767624}
,"flattened":{
"bkid":"hhhfghhfgh"
,"card":"378837837"
,"digest_key":"4a977707829d21dbdb490fae6b7b0ea83eb85371ec7abdd72299fc83016e347c"
,"expires":"2015-09-19"
,"fruit_0":"Egg"
,"fruit_1":"Mange"
,"fruit_2":"Banna"
,"people_0_age":"32"
,"people_0_name":"Amaonwu"
,"people_1_age":"21"
,"people_1_name":"John"
,"school":"Sunnydale School"
,"server":"Linode Sunnydale Server"}
,"computed_hmac":"d15a2c87425699d43b68d8c33ea1eaf052aa1fde94fae14711b5f27f9f617d62"
,"body":{"bkid":"hhhfghhfgh","card":"378837837","expires":"2015-09-19","school":"Sunnydale School","server":"Linode Sunnydale Server","people":[{"name":"Amaonwu","age":"32"},{"name":"John","age":"21"}],"fruit":["Egg","Mange","Banna"],"digest_key":"4a977707829d21dbdb490fae6b7b0ea83eb85371ec7abdd72299fc83016e347c"}}
"""

if __name__ == '__main__':
    # Load the templates data
    data = json.loads(template)

    # Wrap in a try catch block
    engine = PhedorabotWebHook()
    # Set the raw headers, this hsould normally be gotten from you web server
    #
    engine.set_raw_header(data.get('raw_headers'))
    # set the post body
    engine.set_raw_body(json.dumps(data.get('body')))

    try:
        # if we could not verify the payload coming from Phedorabot server
        # we have a problem
        if engine.is_valid_notification():
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
            secret_key = 'we367736536276778'
            # Now set the secret key, so we could verify the payload data
            engine.set_api_secret(secret_key)
            # Try to verify the payload
            if not engine.verify_payload():
                # The payload could not be verified
                raise PhedorabotWebHookException(
                'payload_checksum_error'
                , 'Payload checksum failed data integrity test')
            # We have a valid payload which we can now extract for process
            data = engine.get_payload()
            # use the data to runn the job you wanted to run, ensure that
            # you do not waste time here so that you can send back response
            # to Phedorabot but server on the status of this execution
            # TODO: run you tasks based on the data provided here
            print 'Task running...'
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
        response = engine.build_response()
        # send the response back to Phedorabot server for logs by printing
        # the json encoded version of the response
        print (json.dumps(response))
