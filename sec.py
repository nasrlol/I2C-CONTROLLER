# A speach transcriber using the google speech recognizer and then dsplaying it on the lcd of a raspberry pi

from rpi_lcd import LCD
import RPi.GPIO as GPIO
import speech_recognition as sr
from time import sleep
import sounddevice 
import os

r = sr.Recognizer()
lcd = LCD()
mic = sr.Microphone()

beepPin = 17
allow = False

def stream():
    print("starting live steam")
    # starting the motion live stream
    os.system('motion')


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
        password = "linux"
        while allow == False:
            if words == password:
                allow = True
                print("That's the password!!!")
                stream()
        
    except sr.UnknownValueError:
        lcd.text(error, 1)
        print(error)
    except sr.RequestError:
        lcd.text(r_error, 1)
        print(r_error)
        
def setup():
    print("clearing the lcd screen")
    lcd.clear()
    print("setting up the system")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(beepPin, GPIO.OUT, initial=GPIO.HIGH)
    
def main():
    while True:
        audio = listen_voice()
        recognize_speech(audio)
        GPIO.output(beepPin,GPIO.HIGH)
        sleep(0.5)
        GPIO.output(beepPin,GPIO.LOW)

        

def destroy():
    lcd.clear()

if __name__ == '__main__':
    # Clearing the lcd before starting the program

    print("setting up the alarm")
    setup()
    try:
        main()
    except KeyboardInterrupt:
        destroy()

