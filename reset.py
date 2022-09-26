from machine import Pin
from pimoroni import Buzzer
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER, PEN_RGB565

display = PicoGraphics(display=DISPLAY_PICO_EXPLORER, pen_type=PEN_RGB565)
Buzzer(0).set_tone(0)

