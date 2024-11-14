import time
import os
import speech_recognition as speech
import i2c as LCD
from gpiozero import CPUTemperature

ERROR_BAD_REQUEST = "400 Bad Request"
ERROR_UNAUTHORIZED = "401 Unauthorized"
ERROR_NOT_FOUND = "404 Not Found"
ERROR_TIMEOUT = "408 Request Timeout"

lcd = LCD()
cpu_temp = CPUTemperature()
lama = ollama()
recognizer = speech.Recognizer()
microphone = speech.Microphone()


def display_cpu_info():
    lcd.clear()
    while True:
        load = os.getloadavg()[0]  # 1-minute load average
        temperature = cpu_temp.temperature
        lcd.clear()
        lcd.display_text(f"CPU Load:i {load}", 1)
        lcd.display_text(f"Temp: {temperature:}C", 2)
        time.sleep(5)


def display_uptime():
    lcd.clear()
    with open("/proc/uptime") as f:
        uptime_seconds = float(f.readline().split()[0])
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
    lcd.clear()
    lcd.display_text(f"Uptime: {uptime_str}", 1, "center")


def recognize_speech():
    lcd.clear()
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)
        lcd.clear()
        lcd.display_text(text, 1)
        print("Speech recognized:", text)
    except speech.UnknownValueError:
        lcd.display_text(ERROR_BAD_REQUEST, 1)
        print(ERROR_BAD_REQUEST)
    except speech.RequestError:
        lcd.display_text(ERROR_UNAUTHORIZED, 1)
        print(ERROR_UNAUTHORIZED)


def save_notes():
    PRINT_REQUEST = True
    EXIT_CODES = ['stop', 'break', 'quit', 'exit']
    if PRINT_REQUEST == True:
        while True:
            OUTPUT = input()
            print(OUTPUT)
            lcd.display_text(OUTPUT, 1)
            time.sleep(2)
            for i in EXIT_CODES:
                if OUTPUT == i:
                    PRINT_REQUEST == False



OPTIONS = {
    "CPU_INFO": display_cpu_info(),
    "UPTIME": display_uptime(),
    "SPEECH_TRANSCRIBER": recognize_speech(),
    "NOTES": save_notes(),
}


def main():
    lcd.clear()
    print("WELCOME TO THE I2C COMMAND LINE CENTER")
    print("Options:", ", ".join(OPTIONS.keys()))

    while True:
        user_input = input("Enter command: ").upper()
        action = OPTIONS.get(user_input)

        if action:
            action()
        else:
            lcd.display_text(ERROR_NOT_FOUND, 1)
            print(ERROR_NOT_FOUND)


def destroy():
    lcd.clear()
    os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        destroy()
