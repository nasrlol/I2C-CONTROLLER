import random 
import time
from  rpi_LCD import LCD
import speech_recognition as sr
import sounddevice
import os

LCD = LCD()
VOICE_REC = sr.Recognizer()
MIC = sr.Microphone()
PROCES_LOAD = os.getloadavg()
TIME = current_time.time()

# ERROR CODES
ERROR_BAD_REQUEST = '400'
ERROR_UNAUTHORIZED = '401'
ERROR_NOT_FOUND = '404'
ERROR_TIMEOUT = '408'

def CPU_INFO():
    while (True):
        LCD.tex(PROCES_LOAD(),1)

def CLOCK():
    LCD.text(TIME,1)


