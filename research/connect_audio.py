import os
from twilio.rest import Client
from enum import Enum    

def modifyMeetingNum(meetingNum): 
    strW = "wwww"
    for i in meetingNum:
        strW += i + "w"
    strW += "w#wwwww#wwww#"
    return strW
  
# All Meeting Service Options

class MeetingService(Enum):
    BlueJeans = '+14083179253'
    Zoom = '+14086380968'
    GoogleMeet = '0'
    CiscoWebex = '+18664329903'

def chooseMeetingService(preference):
    try:
        return MeetingService[preference].value
    except:
        print("Meeting Platform is unsupported. Please try again with supported Meeting Platform.")


# Twilio recording call code 

client = Client(account_sid, auth_token)
meetingNum = "wwww6w9w0w8w8w5w6w4w3w0w#wwwww#wwww"
call = client.calls.create(
                        twiml="<Response><Record timeout='45' /></Response>",
                        to='+14083179253',
                        from_='+14049604074',
                        send_digits="ww#ww6w9w0w8w8w5w6w4w3w0w#wwwww#wwww#"
                    )

# Getting access to the recordings
print(call.uri)
print(call.sid)
print(call.subresource_uris["recordings"])

#twiml='<Response><Dial><Number sendDigits="ww#ww6w9w0w8w8w5w6w4w3w0w#wwwww#wwww#">4083179253</Number></Dial></Response>',