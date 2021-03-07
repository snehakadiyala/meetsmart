from google.cloud import speech_v1p1beta1 as speech
import json
client = speech.SpeechClient()

#speech_file = "trial.wav"
# with open(speech_file, "rb") as audio_file:
#     content = audio_file.read()
#audio = speech.RecognitionAudio(content=content)

gcs_uri = "gs://speeches-to-text/interrupted_2.wav"
audio = speech.RecognitionAudio(uri=gcs_uri)
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=48000,
    language_code="en-US",
    enable_speaker_diarization=True,
    diarization_speaker_count=3,
)

print("Waiting for operation to complete...")
response = client.long_running_recognize(config=config, audio=audio)

# The transcript within each result is separate and sequential per result.
# However, the words list within an alternative includes all the words
# from all the results thus far. Thus, to get all the words with speaker
# tags, you only have to take the words list from the last result:

result = response.result().results

result = result[-1]
operation = response.operation
print("Operation: ", operation)

words_info = result.alternatives[0].words
old_speaker = ""
old_end = 0
start = 0
analysis_data = []
transcript = []

for word in words_info:
    tag = word.speaker_tag
    print(word.word, word.speaker_tag)
    if(tag != old_speaker):
        analysis_data.append([tag, start, old_end, transcript])
        start = word.start_time
        transcript = []
    else: 
        transcript.append(word.word)
    old_end = word.end_time
    old_speaker = tag


print(analysis_data)   

with open("results.txt", "w") as txt_file:
    for line in analysis_data:
        txt_file.write(" ".join(str(x) for x in line) + "\n")

print("Completed!")

# words_info = result.alternatives[0].words

# # Printing out the output:
# for word_info in words_info:
#     print(
#         u"word: '{}', speaker_tag: {}".format(word_info.word, word_info.speaker_tag)
#     )

# [(1, 0s, 2.1s), (2, 5s, 7.1s)]
# for speaker_tag: total_time, isInterrupted, interrupts
