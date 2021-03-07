import os
from twilio.rest import Client


def modifyMeetingNum(meetingNum): 
    pass

def chooseMeetingService(preference):
    pass


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "ACdac00567a71b7652ac1988c54044ea8b" #os.environ['TWILIO_ACCOUNT_SID']
auth_token = "5ea34c2ad49473502891ba136012f766" #os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
meetingNum = "wwww6w9w0w8w8w5w6w4w3w0w#wwwww#wwww"
call = client.calls.create(
                        twiml="<Response><Record timeout='45' /></Response>",
                        to='+14083179253',
                        from_='+14049604074',
                        send_digits="ww#ww6w9w0w8w8w5w6w4w3w0w#wwwww#wwww#"
                    )

print(call.sid)

print(call.subresource_uris["recordings"])

#twiml='<Response><Dial><Number sendDigits="ww#ww6w9w0w8w8w5w6w4w3w0w#wwwww#wwww#">4083179253</Number></Dial></Response>',