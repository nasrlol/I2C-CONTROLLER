from smbus import SMBus
from gpiozero import CPUTemperature
import speech_recognition as speech
import os
import time

# LCD Constants
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00
ENABLE_BIT = 0b00000100
LINES = {1: 0x80, 2: 0xC0, 3: 0x94, 4: 0xD4}
ALIGN_FUNC = {"left": "ljust", "right": "rjust", "center": "center"}

# Error Messages
ERROR_BAD_REQUEST = "400 Bad Request"
ERROR_UNAUTHORIZED = "401 Unauthorized"
ERROR_NOT_FOUND = "404 Not Found"
ERROR_TIMEOUT = "408 Request Timeout"

# LCD Control Class
class LCD:
    def __init__(self, address=0x27, bus=1, width=20, rows=4, backlight=True):
        self.address = address
        self.bus = SMBus(bus)
        self.width = width
        self.rows = rows
        self.backlight_status = backlight
        self.delay = 0.0005
        # LCD Initialization
        for cmd in (0x33, 0x32, 0x06, 0x0C, 0x28, 0x01):
            self.write(cmd)
            time.sleep(self.delay)
    def write(self, byte, mode=0):
        """Send a command or character to the LCD."""
        backlight = LCD_BACKLIGHT if self.backlight_status else LCD_NOBACKLIGHT
        self._write_byte(mode | ((byte << 4) & 0xF0) | backlight)
    def _write_byte(self, byte):
        """Write a byte to the I2C bus."""
        self.bus.write_byte(self.address, byte)
        self.bus.write_byte(self.address, (byte | ENABLE_BIT))
        time.sleep(self.delay)
        self.bus.write_byte(self.address, (byte & ~ENABLE_BIT))
        time.sleep(self.delay)
    def display_text(self, text, line=1, align="left"):
        """Display text on a specified line with alignment."""
        self.write(LINES.get(line, LINES[1]))
        aligned_text = getattr(text, ALIGN_FUNC.get(align, "ljust"))(self.width)
        for char in aligned_text:
            self.write(ord(char), mode=1)
    def clear(self):
        """Clear the display."""
        self.write(0x01)
    def set_backlight(self, turn_on=True):
        """Toggle backlight on or off."""
        self.backlight_status = turn_on
        self.write(0)

# Initialize components
lcd = LCD()
cpu_temp = CPUTemperature()
recognizer = speech.Recognizer()
microphone = speech.Microphone()


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
    except speech.UnknownValueError:
        lcd.display_text(ERROR_BAD_REQUEST, line=1)
        print(ERROR_BAD_REQUEST)
    except s.RequestError:
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
