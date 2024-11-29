from smbus import SMBus
from time import sleep
import time
import os
import speech_recognition as sr
from gpiozero import CPUTemperature

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
        self._write_byte(mode | (byte & 0xF0) | backlight_mode)
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



# Error Handling
ERROR_BAD_REQUEST = "the request failed, bad request"
ERROR_UNAUTHORIZED = "you do not have permission to make that request"
ERROR_NOT_FOUND = "the request was not found, try again"
SPEECH_NOT_RECOGNIZED = "we couldn't recognize what you said, try again or \n or check your internet connection" 
ERROR_TIMEOUT = "the request took too long check youre internet connection"

# Initialize components and error handling for debugging
try:
    lcd_instance = lcd.LCD()
except Exception as e:
    print("Error intializing LCD")
try:
    cpu_temp = CPUTemperature()
except Exception as e:
    print("Error initializing CPU temperature sensor:", e)

try: 
    recognizer = sr.Recognizer()
except Exception as e:
    print("Error initialzing voice recognition, its possible the speech recognition module isn't installed")

try:
    microphone = sr.Microphone()
except Exception as e:
    print("Error initialzing the microphone \n check if the sound device package is installed")

# clearing the terminal for a cleaner and program like interaction
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

# Features
def custom_greeting():
    try:
        with open("quotes.txt", "r") as file:
            quotes = [quote.strip() for quote in file.readlines()]
    except FileNotFoundError:
        lcd_instance.text("Quotes file missing", 1)
        return

    for quote in quotes:
        first_line = quote[:16]
        second_line = quote[16:32]
        lcd_instance.text(first_line, 1)
        lcd_instance.text(second_line, 2)
        time.sleep(3)
    lcd_instance.clear()

def joke_of_the_day():
    pass

def pomodoro():
    try:
        duration_minutes = int(input("Enter duration in minutes: "))
        duration_seconds = duration_minutes * 60
        print("Pomodoro started for", duration_minutes, "minutes")
        lcd_instance.text("Pomodoro Running", 1)
        start_count = 0
        count = 0
        while duration_seconds > 0:
            lcd_instance.text(f"Time left: {duration_minutes}:{duration_seconds * 60}", 2)
            time.sleep(1)
            duration_seconds -= 1
            count += 1
            if count == start_count + 60:
                start_count = start
                duration_minutes -= 1

        lcd_instance.text("Time's Up!", 1)
        time.sleep(3)
    except ValueError:
        lcd_instance.text("Invalid input", 1)
        time.sleep(2)

def system_readings():
    while True:
        load = os.getloadavg()[0]
        temperature = cpu_temp.temperature if cpu_temp else "N/A"
        lcd_instance.clear()
        lcd_instance.text(f"CPU Load: {load:.2f}", 1)
        lcd_instance.text(f"Temp: {temperature}C", 2)
        time.sleep(5)

def display_uptime():
    try:
        with open("/proc/uptime") as f:
            uptime_seconds = float(f.readline().split()[0])
        uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
        lcd_instance.text(f"Uptime: {uptime_str}", 1)
        time.sleep(3)
    except Exception as e:
        lcd_instance.text("Error reading uptime", 1)
        print("Error:", e)

def recognize_speech():
    lcd_instance.text("Listening...", 1)
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        output = recognizer.recognize_google(audio)
        lcd_instance.text("Recognized:", 1)
        lcd_instance.text(output[:16], 2)

        print("Speech recognized:", output)
        return output
    except sr.UnknownValueError:
        lcd_instance.text(SPEECH_NOT_RECOGNIZED, 1)
        print(SPEECH_NOT_RECOGNIZED)
    except sr.RequestError as e:
        lcd_instance.text(ERROR_UNAUTHORIZED, 1)
        print(ERROR_UNAUTHORIZED, e)
    except Exception as e:
        lcd_instance.text("Speech Error", 1)
        print("Error:", e)
    return None

def save_notes():
    print("Type your notes (type 'stop' to exit):")
    while True:
        note = input(": ")
        if note.lower() in ["stop", "exit", "quit"]:
            break
        first_line = note[:16]
        second_line = note[16:32]
        lcd_instance.text(first_line, 1)
        lcd_instance.text(second_line, 2)
        time.sleep(3)

# Command center to execute features
def command_center():
    command = recognize_speech().upper()
    if command:
        command()
    else:
        lcd_instance.text(ERROR_NOT_FOUND, 1)
        print(ERROR_NOT_FOUND)
