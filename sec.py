# A speach transcriber using the google speech recognizer and then dsplaying it on the lcd of a raspberry pi

from rpi_lcd import LCD
fro
import speech_recognition as sr
from time import sleep
import sounddevice 
from motion import comp

r = sr.Recognizer()
lcd = LCD()
mic = sr.Microphone()

# Clearing the lcd before starting the program
lcd.clear()

# Listening to the user's voice and putting it into a variable
def listen_voice():
    global audio
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    return audio

# Transcribing the audio to text and printing it out
# Using the google speech recognizer 
# Google speech recognizer does require a internet connection
def recognize_speech(audio):
    error = "400"
    r_error = "401"

    try:
        words = r.recognize_google(audio)
        lcd.text(words, 1)
        print(f"Printing on screen: {words}")
    except sr.UnknownValueError:
        lcd.text(error, 1)
        print(error)
    except sr.RequestError:
        lcd.text(r_error, 1)
        print(r_error)


while True:
    audio = listen_voice()
    recognize_speech(audio)
    

        
                                 
