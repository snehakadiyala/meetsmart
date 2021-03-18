import os
from twilio.rest import Client
from enum import Enum    
import requests



client = Client(account_sid, auth_token)

call_uri = "/2010-04-01/Accounts/ACdac00567a71b7652ac1988c54044ea8b/Calls/CA5975cbd74a3119ae72af049ea9bf7891.json"
sid = "CA5975cbd74a3119ae72af049ea9bf7891"

def get_recording(call_uri, sid, file_name):
    recordings = client.calls.get(sid).recordings.list()
    recording_api_call = "https://api.twilio.com/" + call_uri.split(".json")[0]  + "/Recordings/" + recordings[0].sid
    response = requests.get(recording_api_call)
    wav_file = response.content
    f = open((file_name + ".wav"),"wb")
    f.write(wav_file)
    f.close()
    print(recording_api_call)
    #print(wav_file)

get_recording(call_uri, sid, "test1")

# delete twilio recording deck 
# upload to gcp 
# wipe locally 

#from gcp run ml file 