import time
import os
import speech_recognition as speech
import sounddevice
import bin.hardware_driver as lcd
from gpiozero import CPUTemperature

ERROR_BAD_REQUEST = "400 Bad Request"
ERROR_UNAUTHORIZED = "401 Unauthorized"
ERROR_NOT_FOUND = "404 Not Found"
SPEECH_NOT_RECOGNIZED = "404-1 Speech is not recognized"
ERROR_TIMEOUT = "408 Request Timeout"

lcd_instance = lcd.LCD()
cpu_temp = CPUTemperature()
recognizer = speech.Recognizer()
microphone = speech.Microphone()


# greeting that starts upon the boot of the device:
# shows a hello line; shorter than 16 chars
# and some small information on the second line
def custom_greeting():
    with open('quotes.txt', 'r') as file:
        quotes = file.readlines()

    # Strip newline characters and use the quotes
    quotes = [quote.strip() for quote in quotes]

    # Print the quotes
    for quote in quotes:
        print(quote)
        first_line = ""
        second_line = ""
        count = 0
        for i in quote:
            if count < 16:
                first_line += i
                count += 1
            else:  
                second_line += i
        lcd.text(first_line,1)
        lcd.text(secon_line,2)
def pomodoro():
    time = input("How long do you want to wait? : ")
    print("Okay \nStarting Now...")
    while time > 0:
        time.sleep(1)
        print(time + "Seconds")
        lcd.text(time + " Seconds remaining...", 1)
        time -= 1

    
def weather():
    pass


# ram usage, internet speed,
def system_readings():
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

    return text


def save_notes():
    print("Type your notes (type 'stop' to exit):")
    print("Type line=1 or line=2 to print something to a specific line")
    while True:
        line = 1
        output = input(":")
        output_length = len(output)
        if output.lower() in ["stop", "break", "quit", "exit"]:
            break
        if output == "line=1":
            line = 1
        elif output == "line=2":
            line = 2

        if output_length < 16:
            lcd_instance.text(output, line)
            time.sleep(2)
        else:
            output_list = output.split("")
            first_line = ""
            second_line = ""
            for i in output_list:
                count = 0
                if count > 16:
                    first_line += output_list[i]
                    count += 1
                else:
                    second_line += output_list[i]
        lcd.text(first_line,1)
        lcd.text(secon_line,2)

def command_center(commands):
    # checking if we can reconize commands within the user speech
    # requires ->
    # converting the commands to human readable text
    # no under scars
    command = recognize_speech()
    list = []
    try:
        for i in commands:
            if i == command:
                print("I think i found what you ment...")
                command()
    except:
        print("ERROR 404 - COMMAND NOT RECOGNIZED")


FEATURES = {
        "READINGS": system_readings,
        "UPTIME": display_uptime,
        "SPEECH_TRANSCRIBER": recognize_speech,
        "NOTES": save_notes,
        "COMMAND CENTER": command_center,
        }


def main():
    lcd_instance.clear()
    os.system("cls" if os.name == "nt" else "clear")
    print("FEATURES:", ", ".join(FEATURES.keys()))

    while True:
        user_input = input("Enter command: ").upper()
        action = FEATURES.get(user_input)

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
