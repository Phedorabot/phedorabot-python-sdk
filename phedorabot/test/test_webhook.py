from phedorabot.webhook import PhedorabotWebHook
from phedorabot.webhook import PhedorabotWebHookException
import json

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
        # Try verify that the notification isa valid one by checking for the
        # api key in the header of the request
        engine.is_valid_notification()()
        
        if engine.is_valid_notification():
            # We have a notification that is targetted at a given api key
            # get the target api key and use that to find its
            # corresponding api secret key, we need this to verify that the
            # payload is valid

            api_key = engine.get_api_key()
            if not api_key or not len(api_key):
                raise ValueError(
                'api key is not defined in this notification header')

            # Now load this api key corresponding api secret, the webhook needs
            # it to verify the authenticity of the payload as coming from
            # Phedorabot server
            msecret = 'we367736536276778'
            engine.set_api_secret(msecret)
            # verify the payload
            if engine.verify_payload():
                # At this point we know that the payload is actually coming from
                # Phedorabot and we can now use it to perform that task that
                # needs to be done

                payload = engine.get_payload()
                # TODO: work with the payload

    except (Exception, ValueError, PhedorabotWebHookException) as ex:
        print ex
    finally:
        # Always try to build response whether the passing fails or not
        # so that you can review what happened
        response = engine.build_response()
        print response
