import time
import os
import speech_recognition as sr
from gpiozero import CPUTemperature

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
    print(
        "Error initialzing voice recognition, its possible the speech recognition module isn't installed"
    )

try:
    microphone = sr.Microphone()
except Exception as e:
    print(
        "Error initialzing the microphone \n check if the sound device package is installed"
    )


class fe:

    def __init__(self):
        self.clear_terminal = clear_terminal()
        self.custom_greeting = custom_greeting()
        self.joke_of_the_day = joke_of_the_day()
        self.pomodoro = pomodoro()
        self.system_readings = system_readings()
        self.display_uptime = display_uptime()
        self.recognize_speech = recognize_speech()
        self.save_notes = save_notes()
        self.command_center = command_center()

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
                lcd_instance.text(
                    f"Time left: {duration_minutes}:{duration_seconds * 60}", 2
                )
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
