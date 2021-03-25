
import numpy as np
import pandas as pd
import os
import pickle
from google.cloud import storage
import librosa
import sklearn
import json

gcs = storage.Client()
bucket = gcs.get_bucket('ami_corpus')

def preprocess(new_file_path):
    x, sr = librosa.load(new_file_path)
    mfccs = librosa.feature.mfcc(x, sr=sr)
    mfccs = sklearn.preprocessing.scale(mfccs, axis=1)
    print(mfccs.shape)
    mfccs = mfccs.flatten().reshape(1,-1)
    return mfccs

def download_file(file_path, file_name):

    blob = bucket.blob(file_path)
    
    folder = '/tmp/'
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    new_file_path = folder + file_name
    blob.download_to_filename(new_file_path)
    
    return new_file_path 

def predict(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    print("Entered")
    
    request = request.get_json()
    meeting_wav_file_name = request["meeting_wav_file_name"]
    model_name =  "initial_model.pkl"

    new_file_name = "chunk.wav"
    file_path = download_file('meeting_files/'+ meeting_wav_file_name, new_file_name)
    features = preprocess(file_path)
    
    new_model_name = "local_model.pkl"
    model_path = download_file('models/' + model_name, new_model_name)
    print("downloaded locally 2")
    
    
    model = pickle.load(open(model_path, 'rb'))
    
    preds = model.predict(features)
    
    return preds
    
# predict(json.dumps({"meeting_wav_file_name": "audio_chunk_0_136.wav"}))

