import threading
import queue
import time
import datetime
import pyaudio
import speech_recognition as sr

# initialize the audio queue
audio_queue = queue.Queue()

# define the audio callback for the PC input device
def pc_audio_callback(in_data, frame_count, time_info, status):
    audio_queue.put(in_data)
    return (None, pyaudio.paContinue)

# define the audio transcription function
def transcribe_audio():
    # initialize the SpeechRecognition recognizer
    r = sr.Recognizer()
    r.energy_threshold = 4000

    while True:
        # wait for audio data to be available in the queue
        audio_data = audio_queue.get()
        
        # check if the audio data is from the PC input device
        if audio_data == 'STOP':
            break
        elif audio_data.startswith('PC'):
            audio_data = audio_data[2:]
            audio = sr.AudioData(audio_data, 16000, 2)
            source = r.record(audio)
            text = r.recognize_google(source)
            with open(f"PC_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt", "a") as f:
                f.write(f"PC: {text}\n")
        # assume audio data is from the user input (microphone)
        else:
            audio = sr.AudioData(audio_data, 16000, 2)
            source = r.record(audio)
            text = r.recognize_google(source)
            with open(f"User_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt", "a") as f:
                f.write(f"User: {text}\n")

# start the audio transcription thread
transcription_thread = threading.Thread(target=transcribe_audio)
transcription_thread.start()

# start the PC input audio stream
audio_interface = pyaudio.PyAudio()
pc_stream = audio_interface.open(format=pyaudio.paInt16, channels=2, rate=16000, input=True, stream_callback=pc_audio_callback)

# start the user input audio stream
with sr.Microphone(device_index=0) as mic:
    try:
        while True:
            print("Speak now or press Ctrl-C to stop...")
            audio_data = mic.record(phrase_time_limit=10)
            audio_data = audio_data.frame_data
            audio_queue.put(audio_data)
    except KeyboardInterrupt:
        pass

# stop the PC input audio stream and transcription thread
pc_stream.stop_stream()
pc_stream.close()
audio_queue.put('STOP')
transcription_thread.join()

# close the audio interface
audio_interface.terminate()
