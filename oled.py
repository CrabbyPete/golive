import time

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

from PIL import ImageFont

class OLED:
    def __init__(self):
        serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(serial)

    def clear(self):
        pass

    def write(self, message):
        font = ImageFont.truetype("arial.ttf", 20)
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline="black", fill="black")
            top = 4
            for line in message:
                draw.text((4, top), line, font=font, fill="white")
                top += 22


def main():
    oled = OLED()
    oled.write("Ready")
    while True:
        time.sleep(5)

if __name__ == "__main__":
    main()