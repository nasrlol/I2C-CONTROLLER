import smbus2 as SMBus
import time

LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00
ENABLE_BIT = 0b00000100
LINES = {1: 0x80, 2: 0xC0}
ALIGN_FUNC = {"left": "ljust", "right": "rjust", "center": "center"}


class LCD:

    def __init__(self, address=0x27, bus=1, width=20, rows=4, backlight=True):
        self.address = address
        self.bus = SMBus(bus)
        self.width = width
        self.rows = rows
        self.backlight_status = backlight
        self.delay = 0.0005

        for cmd in (0x33, 0x32, 0x06, 0x0C, 0x28, 0x01):
            self.write(cmd)
            time.sleep(self.delay)

    def write(self, byte, mode=0):
        backlight = LCD_BACKLIGHT if self.backlight_status else LCD_NOBACKLIGHT
        self._write_byte(mode | ((byte << 4) & 0xF0) | backlight)

    def _write_byte(self, byte):
        self.bus.write_byte(self.address, byte)
        self.bus.write_byte(self.address, (byte | ENABLE_BIT))
        time.sleep(self.delay)
        self.bus.write_byte(self.address, (byte & ~ENABLE_BIT))
        time.sleep(self.delay)

    def display_text(self, text, line=1, align="left"):
        self.write(LINES.get(line, LINES[1]))
        aligned_text = getattr(text, ALIGN_FUNC.get(align, "ljust"))(self.width)
        for char in aligned_text:
            self.write(ord(char), mode=1)

    def clear(self):
        self.write(0x01)

    def set_backlight(self, turn_on=True):
        self.backlight_status = turn_on
        self.write(0)
