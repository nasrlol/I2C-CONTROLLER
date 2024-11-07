from smbus2 import SMBus
from time import sleep
from gpiozero import CPUTemperature
from rpi_lcd import LCD

import speech_recognition as sr
import sounddevice
import os

ALIGN_FUNC = {
    'left': 'ljust',
    'right': 'rjust',
    'center': 'center'}
CLEAR_DISPLAY = 0x01
ENABLE_BIT = 0b00000100
LINES = {
    1: 0x80,
    2: 0xC0,
    3: 0x94,
    4: 0xD4}

LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

ERROR_BAD_REQUEST = '400'
ERROR_UNAUTHORIZED = '401'
ERROR_NOT_FOUND = '404'
ERROR_TIMEOUT = '408'

class LCD(object):

    def __init__(self, address=0x27, bus=1, width=20, rows=4, backlight=True):
        self.address = address
        self.bus = SMBus(bus)
        self.delay = 0.0005
        self.rows = rows
        self.width = width
        self.backlight_status = backlight

        self.write(0x33)
        self.write(0x32)
        self.write(0x06)
        self.write(0x0C)
        self.write(0x28)
        self.write(CLEAR_DISPLAY)
        sleep(self.delay)

    def _write_byte(self, byte):
        self.bus.write_byte(self.address, byte)
        self.bus.write_byte(self.address, (byte | ENABLE_BIT))
        sleep(self.delay)
        self.bus.write_byte(self.address,(byte & ~ENABLE_BIT))
        sleep(self.delay)

    def write(self, byte, mode=0):
        backlight_mode = LCD_BACKLIGHT if self.backlight_status else LCD_NOBACKLIGHT
        self._write_byte(mode | ((byte << 4) & 0xF0) | backlight_mode)

    def text(self, text, line, align='left'):
        self.write(LINES.get(line, LINES[1]))
        text, other_lines = self.get_text_line(text)
        text = getattr(text, ALIGN_FUNC.get(align, 'ljust'))(self.width)
        for char in text:
            self.write(ord(char), mode=1)
        if other_lines and line <= self.rows - 1:
            self.text(other_lines, line + 1, align=align)

    def backlight(self, turn_on=True):
        self.backlight_status = turn_on
        self.write(0)

    def get_text_line(self, text):
        line_break = self.width
        if len(text) > self.width:
            line_break = text[:self.width + 1].rfind(' ')
        if line_break < 0:
            line_break = self.width
        return text[:line_break], text[line_break:].strip()

    def clear(self):
        self.write(CLEAR_DISPLAY)

LCD_DISPLAY = LCD()
VOICE_REC = sr.Recognizer()
MIC = sr.Microphone()
PROCES_LOAD = os.getloadavg()
TIME = current_time.time()
UPTIME = time.CLOCK_UPTIME()
CPU_TEMP = CPUTemperature()

# clearing the lcd from any text that was on it before the program started to ensure smooth operations
lcd.clear()

# Listening to the user's voice and putting it into a variable
def listen_voice():
    global audio
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    return audio

# Transcribing the audio to text and printing it out
# Using the Google Speech Recognizer 
def recognize_speech(audio):
    try:
        words = r.recognize_google(audio)
        LCD_DISPLAY.text(words, 1)
        print(f"Printing on screen: {words}")
    except sr.UnknownValueError:
        LCD_DISPLAY.text(ERROR_BAD_REQUEST, 1)
        print(ERROR_BAD_REQUEST)
    except sr.RequestError:
        LCD_DISPLAY.text(ERROR_UNAUTHORIZED, 1)
        print(ERROR_UNAUTHORIZED)                                 

def CPU_INFO():
    print("you chose to display the cpou")
    while (True):
        LCD.text(PROCES_LOAD(),1,left)

def CURRENT_TIME():
    while True:
        backlight_mode = True
        LCD.text(TIME,2,center)

def UPTIME():
    while True:
        LCD.text(UPTIME,1,left)

def CPU_TEMP():
    while True:
        LCD.text(cpu.temperature)

def CPU_LOAD():
    backlight_mode = True
    LCD.text(PROCES_LOAD,1,left)

def NOTES():
    count = 0
    user_notes = input()
    for i in user_notes:
        while count < 20:
            lcd.text(i,1,left)
            count += 1

            
OPTIONS = ["CPU_CLOCK", "TIME", "UPTIME", "CPU_TEMP", "CPU_LOAD", "NOTES", "SPEECH_TRANSCRIBER"]

def PROGRAM(USER_INPUT):
    print("WELCOME TO THE I2C COMMAND LINE CENTER \n WHAT DO YOU WISH TO DO? ")
    print(OPTIONS)

    FOUND = False
    while FOUND == False:

        USER_INPUT = input().upper()
        for i in OPTIONS:
            if i == USER_INPUT:
                FOUND = True
            else:
                print(ERROR_NOT_FOUND)

PROGRAM()