import os
from twilio.rest import Client
from enum import Enum    
import requests
from google.cloud import storage


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
    return recordings[0].sid
    #print(wav_file)

def delete_recording(call_uri, recording_sid):
    delete_api_call = "https://api.twilio.com/" + call_uri.split("/Calls")[0] + "/Recordings/" + recording_sid
    requests.delete(delete_api_call)

def upload_blob(bucket_name, source_file_name, destination_blob_name):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

# def get_speaker_timings():
# def get_speaker_variance():
# def split_wav():
# def get_preds_for_wavs():

"""Uploads a file to the bucket."""
file_name = "test1"
bucket_name = "ami_corpus"
source_file_name = file_name + ".wav"
destination_blob_name = "meeting_files"

recording_sid = get_recording(call_uri, sid, file_name)
delete_recording(call_uri, recording_sid)

# upload to gcp 
upload_blob(bucket_name, source_file_name, destination_blob_name)

# wipe locally 
os.remove(source_file_name)

# get speaker diarization results for speaker_split 


#from gcp run ml file 

url = "https://us-central1-silicon-webbing-306013.cloudfunctions.net/basic_overlap_prediction"
param = {"meeting_wav_file_name": source_file_name}

requests.get(url, json=param)