
from pydub import AudioSegment
from .retrieve_recording import upload_blob


def get_split_centers(seconds):
    return [sec for sec in range(1, int(seconds*100)-1, 500)]

def process_recording(sound_files):
    counter = 0
    
    for sound_file in sound_files:
        sound = AudioSegment.from_wav(sound_file)
        for time in get_split_centers(sound.duration_seconds): 
            audio_chunk=sound[time-500:time+500]
            sound_file_name = sound_file.split(".wav")[0]
            file_name = "{}_{}_{}.wav".format(sound_file, time-500, time+500)
            audio_chunk.export(file_name, format="wav")
            upload_blob("ami_corpus", file_name, "meeting_files/" + sound_file_name + "/audio_chunks/" + file_name)
            counter += 1
        
         
        upload_blob("ami_corpus", sound_file, "meeting_files/" + sound_file_name + "/" + sound_file)


def generate_single_meeting_report(sound_file, speaker_count):
    report = {}

    report.update({"speaker_identification_clips" : 0 }) # get_speaker_voices
    report.update({"dual_confirmed_interruptions" : 0 }) # get_interruptions [(time_stamp, interruptor, interruptee)]
    report.update({"speaker_time_statistics" : 0 }) # get_speaker_stats(sound_file, speaker_count)
    report.update({"interruption_statistcs" : 0}) #get_interruption_stats(interruption_array)

    return report




