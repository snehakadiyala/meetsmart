from google.cloud import speech_v1p1beta1 as speech
import json
import numpy as np
import requests
from pydub import AudioSegment
from .retrieve_recording import upload_blob
from google.cloud import storage
import datetime

#speech_file = "trial.wav"
# with open(speech_file, "rb") as audio_file:
#     content = audio_file.read()
#audio = speech.RecognitionAudio(content=content)

# gcs_uri = "gs://speeches-to-text/interrupted_2.wav"

# audio = speech.RecognitionAudio(uri=gcs_uri)
# config = speech.RecognitionConfig(
#     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#     sample_rate_hertz=48000,
#     language_code="en-US",
#     enable_speaker_diarization=True,
#     diarization_speaker_count=3,
# )

# print("Waiting for operation to complete...")
# response = client.long_running_recognize(config=config, audio=audio)

words = 0

def download_blob(gcs_location):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("ami_corpus")
    blob = bucket.blob(gcs_location)
    location = "/tmp/{}".format(gcs_location.split("/")[-1])
    blob.download_to_filename(location)

    return location


def get_speaker_diarization_results(source_file_name, speaker_count):
    client = speech.SpeechClient()
    
    gcs_uri = "gs://ami_corpus/meeting_files/" + source_file_name
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="en-US",
        enable_speaker_diarization=True,
        diarization_speaker_count=speaker_count,
    )
    response = client.long_running_recognize(config=config, audio=audio)
    result = response.result().results[-1]
    return result.alternatives[0].words


def get_speaker_stats(speaker_count, words=words):

    stats = {}
    # Get Total Speaker Minutes 
    timing = [0] * speaker_count
    for word in words: 
        timing[word.speaker_tag-1] += (word.end_time - word.start_time).total_seconds() 
    timing =  [time / 60 for time in timing]

    # Speaker Average Spoken Time 
    average = np.average(timing)

    # Speaker Variance
    variance = np.var(timing)

    # Speaker Standard Deviation 
    stdev = np.std(timing)

    stats.update({"speaker_minutes" : timing})
    stats.update({"average_speaker_time" : average})
    stats.update({"variance_speaker_time" : variance})
    stats.update({"standard_deviation_speaker_time" : stdev})

    return stats

def create_speaker_clips(sound_file_name, gcs_path, speaker_count, words):
    speaker_clips = [None] * speaker_count

    second_counter = 0
    prev_speaker_tag = None
    for word in words: 
        
        if((prev_speaker_tag == None or prev_speaker_tag == word.speaker_tag) and not speaker_clips[word.speaker_tag-1]):
            prev_speaker_tag = word.speaker_tag
            second_counter += (word.end_time - word.start_time).total_seconds() 
            
            if (second_counter >= 1): 
                speaker_clips[prev_speaker_tag-1] = (word.end_time.total_seconds() - second_counter, word.end_time.total_seconds())
                prev_speaker_tag = None
                second_counter = 0
        
        else:
            prev_speaker_tag = word.speaker_tag
            second_counter = 0
    
    for idx, clip in enumerate(speaker_clips):
        if(clip != None): 
            sound = AudioSegment.from_wav(download_blob(gcs_path))
            audio_chunk = sound[int(clip[0]*1000):int(clip[1]*1000)]
            audio_chunk_name = "speaker_{}_clip.wav".format(idx)
            audio_chunk.export(audio_chunk_name, format="wav")
            upload_blob("ami_corpus", audio_chunk_name, "meeting_files/{}/speaker_clips/{}".format(sound_file_name, audio_chunk_name))
    
    return True


def get_dual_confirmed_interruptions(sound_file_name, words): 
    # timestamp_tuples which show where there might be interruptions 
    model_overlap_timestamps = get_speech_overlap_timestamps(sound_file_name)
    # timestamp_tuples
    speaker_change_times = get_speaker_changes(words) 

    confirmed_interruptions = []
    for time in speaker_change_times: 
        for time_range in model_overlap_timestamps:
            if time[2] in range(time_range[0], time_range[1]): 
                confirmed_interruptions.append((time[0], time[1]))



def get_speech_overlap_timestamps(sound_file_name):
    url = "https://us-central1-silicon-webbing-306013.cloudfunctions.net/basic_overlap_prediction"
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("ami_corpus")
    sound_file_name = sound_file_name.split(".wav")[0]

    overlaps = []
    
    for blob in bucket.list_blobs(prefix= 'meeting_files/{}/audio_chunks'.format(sound_file_name)):
        if(blob.name.endswith(".wav")):
            param = {"meeting_wav_file_name": blob.name}
            if(requests.post(url, json=param).json()["preds"] == 1):
                time_stamps = blob.name.split("_")
                time_stamps = (int(time_stamps[1])/1000.0, int(time_stamps[2].replace(".wav",""))/1000.0)
                overlaps.append(time_stamps)

    return overlaps

def get_speaker_changes(words): 
    old_speaker = ""
    old_end = datetime.timedelta(0)
    analysis_data = []
    transcript = []

    for word in words:
        tag = word.speaker_tag
        #print(word.word, word.speaker_tag)
        if(tag != old_speaker):
            analysis_data.append((old_speaker, tag, old_end.total_seconds()))
            transcript = []
        else: 
            transcript.append(word.word)
        old_end = word.end_time
        old_speaker = tag

    return analysis_data

def get_interruption_stats(interruptions): 

    interruptees, interrupted = zip(**interruptions)

    interruptees = {x: interruptees.count(x) for x in interruptees}

    interrupted = {x: interrupted.count(x) for x in interrupted}



    

# TESTING CODE -------------------------------------------------------------------------------------------------

# The transcript within each result is separate and sequential per result.
# However, the words list within an alternative includes all the words
# from all the results thus far. Thus, to get all the words with speaker
# tags, you only have to take the words list from the last result:

# result = response.result().results

# result = result[-1]
# operation = response.operation
# print("Operation: ", operation)

# words_info = result.alternatives[0].words
# old_speaker = ""
# old_end = 0
# start = 0
# analysis_data = []
# transcript = []

# for word in words_info:
#     tag = word.speaker_tag
#     print(word.word, word.speaker_tag)
#     if(tag != old_speaker):
#         analysis_data.append([tag, start, old_end, transcript])
#         start = word.start_time
#         transcript = []
#     else: 
#         transcript.append(word.word)
#     old_end = word.end_time
#     old_speaker = tag


# print(analysis_data)   

# with open("results.txt", "w") as txt_file:
#     for line in analysis_data:
#         txt_file.write(" ".join(str(x) for x in line) + "\n")

# print("Completed!")

# words_info = result.alternatives[0].words

# # Printing out the output:
# for word_info in words_info:
#     print(
#         u"word: '{}', speaker_tag: {}".format(word_info.word, word_info.speaker_tag)
#     )

# [(1, 0s, 2.1s), (2, 5s, 7.1s)]
# for speaker_tag: total_time, isInterrupted, interrupts
