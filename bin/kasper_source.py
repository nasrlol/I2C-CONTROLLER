from smbus import SMBus
import gpiozero
from gpiozero import CPUTemperature
import speech_recognition as sr
import os
import time

Initialize components
lcd = LCD()
cpu_temp = CPUTemperature()
recognizer = sr.Recognizer()
microphone = sr.Microphone()


# Display Functions
def display_cpu_info():
    """Display CPU load and temperature on the LCD."""
    while True:
        load = os.getloadavg()[0]  # 1-minute load average
        temperature = cpu_temp.temperature
        lcd.clear()
        lcd.display_text(f"CPU Load: {load:.2f}", line=1)
        lcd.display_text(f"Temp: {temperature:.1f}C", line=2)
        time.sleep(5)


def display_uptime():
    """Display system uptime on the LCD."""
    with open("/proc/uptime") as f:
        uptime_seconds = float(f.readline().split()[0])
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
    lcd.clear()
    lcd.display_text(f"Uptime: {uptime_str}", line=1)


def recognize_speech():
    """Capture and transcribe speech input."""
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)
        lcd.clear()
        lcd.display_text(text, line=1)
        print("Speech recognized:", text)
    except sr.UnknownValueError:
        lcd.display_text(ERROR_BAD_REQUEST, line=1)
        print(ERROR_BAD_REQUEST)
    except sr.RequestError:
        lcd.display_text(ERROR_UNAUTHORIZED, line=1)
        print(ERROR_UNAUTHORIZED)


# Main Program Options
OPTIONS = {
    "CPU_INFO": display_cpu_info,
    "UPTIME": display_uptime,
    "SPEECH_TRANSCRIBER": recognize_speech,
}


def main():
    # Main program loop to accept user commands.
    print("WELCOME TO THE I2C COMMAND LINE CENTER")
    print("Options:", ", ".join(OPTIONS.keys()))

    while True:
        user_input = input("Enter command: ").upper()
        action = OPTIONS.get(user_input)

        if action:
            action()
        else:
            lcd.display_text(ERROR_NOT_FOUND, line=1)
            print(ERROR_NOT_FOUND)


if __name__ == "__main__":
    main()
