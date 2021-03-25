
from pydub import AudioSegment

def get_split_centers(seconds):
    return [sec for sec in range(1, int(seconds*100)-1, 500)]

def process_recording(sound_files, speaker_change_times):
    counter = 0
    
    for sound_file in sound_files:

        sound = AudioSegment.from_wav(sound_file)
        for time in get_split_centers(sound.duration_seconds): 
            audio_chunk=sound[time-500:time+500]
            audio_chunk.export( "tmp_files/{}_{}_{}.wav".format(sound_file.split(".wav")[0], time-500, time+500), format="wav")
            counter += 1
        
        #upload full_file to GCP, upload chunks to gcp 
   
def generate_report(sound_file, speaker_count):
    report = {}

    report.update({"speaker_identification_clips" : 0 }) # get_speaker_voices
    report.update({"dual_confirmed_interruptions" : 0 }) # get_interruptions [(time_stamp, interruptor, interruptee)]
    report.update({"speaker_time_statistics" : 0 }) # get_speaker_stats(sound_file, speaker_count)
    report.update({"interruption_statistcs" : 0}) #get_interruption_stats(interruption_array)

    return report

# get_speaker_diarization_results()

# get_overlap_results()

# get_dual_confirmed_interruptions()


