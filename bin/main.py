import time
import os
import speech_recognition as speech
import sounddevice
import i2c as lcd
from gpiozero import CPUTemperature

ERROR_BAD_REQUEST = "400 Bad Request"
ERROR_UNAUTHORIZED = "401 Unauthorized"
ERROR_NOT_FOUND = "404 Not Found"
ERROR_TIMEOUT = "408 Request Timeout"

lcd_instance = lcd.LCD()
cpu_temp = CPUTemperature()
recognizer = speech.Recognizer()
microphone = speech.Microphone()


def display_cpu_info():
    lcd_instance.clear()
    while True:
        load = os.getloadavg()[0]
        temperature = cpu_temp.temperature
        lcd_instance.clear()
        lcd_instance.text(f"CPU Load: {load}", 1)
        lcd_instance.text(f"Temp: {temperature:.1f}C", 2)
        time.sleep(5)


def display_uptime():
    lcd_instance.clear()
    with open("/proc/uptime") as f:
        uptime_seconds = float(f.readline().split()[0])
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
    lcd_instance.clear()
    lcd_instance.text(f"Uptime: {uptime_str}", 1, "center")


def recognize_speech():
    lcd_instance.clear()
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)
        lcd_instance.clear()
        lcd_instance.text(text, 1)
        print("Speech recognized:", text)
    except speech.UnknownValueError:
        lcd_instance.text(ERROR_BAD_REQUEST, 1)
        print(ERROR_BAD_REQUEST)
    except speech.RequestError:
        lcd_instance.text(ERROR_UNAUTHORIZED, 1)
        print(ERROR_UNAUTHORIZED)


def save_notes():
    print("Type your notes (type 'stop' to exit):")
    print("Type line=1 or line=2 to print something to a specific line")
    while True:
        line = 1
        output = input(":")
        if output.lower() in ["stop", "break", "quit", "exit"]:
            break
        if output == "line=1":
            line = 1
        elif output == "line=2":
            line = 2
        lcd_instance.text(output, line)
        time.sleep(2)


OPTIONS = {
    "CPU_INFO": display_cpu_info,
    "UPTIME": display_uptime,
    "SPEECH_TRANSCRIBER": recognize_speech,
    "NOTES": save_notes,
}


def main():
    lcd_instance.clear()
    print("WELCOME TO THE I2C COMMAND LINE CENTER")
    print("Options:", ", ".join(OPTIONS.keys()))

    while True:
        user_input = input("Enter command: ").upper()
        action = OPTIONS.get(user_input)

        if action:
            action()
        else:
            lcd_instance.text(ERROR_NOT_FOUND, 1)
            print(ERROR_NOT_FOUND)


def destroy():
    lcd_instance.clear()
    os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        destroy()
