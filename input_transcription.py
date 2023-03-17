import os
import speech_recognition as sr
from datetime import datetime

# create a recognizer object
r = sr.Recognizer()

# use the default microphone as the audio source
mic = sr.Microphone()

# get the current date and time for the filename
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

# create a new text file with the current date
filename = f"Transcritps\{current_date}.txt"

# check if the file already exists for the current day
if os.path.isfile(filename):
    file_mode = "a"
else:
    file_mode = "w"

# open the file in append mode if it already exists, or in write mode if it doesn't
file = open(filename, file_mode, encoding="utf-8")

# write the instructions to the file if it's a new file
if file_mode == "w":
    file.write("Speak now or press Ctrl-C to stop...\n\n")

try:
    while True:
        # listen for audio input from the microphone
        with mic as source:
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = r.listen(source)

        # recognize speech using Google Speech Recognition
        try:
            text = r.recognize_google(audio, language="ja-JP")

            # print the recognized text
            print(f"You said: {text}\n")

            # write the recognized text to the file
            file.write(f"{text}\n\n")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
except KeyboardInterrupt:
    # close the file when the user stops the program
    file.close()
    print(f"\nRecording stopped. Audio saved to {filename}.")
