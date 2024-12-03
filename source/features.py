import time
import os
import speech_recognition as sr
from gpiozero import CPUTemperature
import hardware_driver as lcd  # importing the ./hardware_driver.py file

# some functions need to be put on a different thread but we are keeping that project for another time
# import threading

# Error Handling
ERROR_BAD_REQUEST = "the request failed, bad request"
ERROR_UNAUTHORIZED = "you do not have permission to make that request"
ERROR_NOT_FOUND = "the request was not found, try again"
SPEECH_NOT_RECOGNIZED = "we couldn't recognize what you said, try again or \n or check your internet connection"
ERROR_TIMEOUT = "the request took too long check youre internet connection"


# Initialize components and error handling for debugging
# try initializingthe lcd
# if initializations fail they should disale they're function

L = lcd.LCD()

# try initializing the temperature readings
try:
    cpu_temp = CPUTemperature()

except Exception as e:
    print("Error initializing CPU temperature sensor:", e)


# try initializing the google speech recognizer
try:
    recognizer = sr.Recognizer()

except Exception as e:
    print(
        "Error initialzing voice recognition, its possible the speech recognition module isn't installed"
    )


# try initializing the microphone
try:
    microphone = sr.Microphone()

except Exception as e:
    print(
        "Error initialzing the microphone \n check if the sound device package is installed"
    )


class feat:

    def __init__(self):
        pass

    # clearing the terminal for a cleaner and program like interaction
    def clear_terminal_lcd(self):
        lcd.instance.clear()
        os.system("cls" if os.name == "nt" else "clear")

    # Features
    def custom_greeting(self):
        self.clear_terminal_lcd()
        try:
            with open("quotes.txt", "r") as file:
                quotes = [quote.strip() for quote in file.readlines()]
        except FileNotFoundError:
            L.text("Quotes file missing", 1)
            return

        for quote in quotes:
            first_line = quote[:16]
            second_line = quote[16:32]
            L.text(first_line, 1)
            L.text(second_line, 2)
            time.sleep(3)
        L.clear()

    def pomodoro(self):

        self.clear_terminal_lcd()
        try:
            duration_minutes = int(input("Enter duration in minutes: "))
            duration_seconds = duration_minutes * 60

            print("Pomodoro started for", duration_minutes, "minutes")

            time_passed_seconds = 0
            time_passed_minutes = 0

            while duration_seconds > 0:
                if duration_minutes != 0:
                    duration_minutes -= 1
                time_passed_seconds += 1
                duration_seconds -= 1
                if time_passed_seconds == 60:
                    duration_minutes -= 1
                    time_passed_seconds == 0
                print(f"\ryou have {duration_minutes}:{duration_seconds} left", end="")
                L.text(f"\ryou have {duration_minutes}:{duration_seconds} left", 1)
                sleep(1)

        except ValueError:
            L.text("Invalid input", 1)
            time.sleep(2)

    def temperature(self):
        self.clear_terminal_lcd()
        while True:
            load = os.getloadavg()[0]
            temperature = cpu_temp.temperature if cpu_temp else "N/A"
            L.clear()
            L.text(f"CPU Load: {load:.2f}", 1)
            L.text(f"Temp: {temperature}C", 2)
            time.sleep(5)

    def display_uptime(self):
        self.clear_terminal_lcd()
        try:
            with open("/proc/uptime") as f:
                uptime_seconds = float(f.readline().split()[0])
            uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
            L.text(f"Uptime: {uptime_str}", 1)
            time.sleep(3)
        except Exception as e:
            L.text("Error reading uptime", 1)
            print("Error:", e)

    def recognize_speech(self, recognizer_):
        self.clear_terminal_lcd()

        L.text("Listening...", 1)
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            output = recognizer.recognize_google(audio)
            L.text("Recognized:", 1)
            L.text(output[:16], 2)

            print("Speech recognized:", output)
            return output
        except sr.UnknownValueError:
            L.text(SPEECH_NOT_RECOGNIZED, 1)
            print(SPEECH_NOT_RECOGNIZED)
        except sr.RequestError as e:
            L.text(ERROR_UNAUTHORIZED, 1)
            print(ERROR_UNAUTHORIZED, e)
        except Exception as e:
            L.text("Speech Error", 1)
            print("Error:", e)
        return None

    def save_notes(self):
        self.clear_terminal_lcd()
        print("Type your notes (type 'stop' to exit):")
        while True:
            note = input(": ")
            if note.lower() in ["stop", "exit", "quit"]:
                break
            first_line = note[:16]
            second_line = note[16:32]
            L.text(first_line, 1)
            L.text(second_line, 2)
            time.sleep(3)

    # Command center to execute features
    def command_center(self):
        self.clear_terminal_lcd()
        command = self.recognize_speech().lower()
        if command == "greeting" or command == "greetings":
            self.custom_greeting()
        elif command == "uptime":
            self.display_uptime()
        elif command == "pomodoro" or command == "pomodoro":
            self.pomodoro()
        elif command == "speech" or "transcribe":
            self.recognize_speech()
        elif command == "save notes" or command == notes:
            self.save_notes()
        elif command == "temperature":
            self.temperature()
        else:
            L.text(ERROR_NOT_FOUND, 1)
            print(ERROR_NOT_FOUND)
