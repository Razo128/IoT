# Package import
from machine import Pin
from pimoroni import Buzzer
import time
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER, PEN_RGB565

# Display setup
display = PicoGraphics(display=DISPLAY_PICO_EXPLORER, pen_type=PEN_RGB565)

WIDTH, HEIGHT = display.get_bounds()

# Pen Creation
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
RED = display.create_pen(255, 0 ,0)
BLUE = display.create_pen(0, 0, 255)

# Input
ldr = machine.ADC(27)

# Audio output
buzz = Buzzer(0)

# Progress variables
tick = -1
tick_read_dict = {}

# Pixel display size
pix_size = 5 # odd numbers only

# Light level bounds settings
too_bright = 400 # (>100, <=650)
too_dark = 1000 # (<1300, >= 750)

brt_rng = int(too_bright - 100)
drk_rng = int(1300 - too_dark)

while False:
    display = PicoGraphics(display=DISPLAY_PICO_EXPLORER, pen_type=PEN_RGB565)
    Buzzer(0).set_tone(0)

while True:   
    value = str(ldr.read_u16()) # String version of readings for printout
    #print(value) # Console printout of readings
    tick += 1 # Tick Progresser
    tick_read_dict[tick*pix_size] = int(260-((pix_size-1)/2)-(ldr.read_u16()/5))
    # ^Pairs light readings with ticks (both converted to screen display values)^
    #print(tick_read_dict)
    
    # Set up screen colours
    display.set_pen(WHITE)  
    display.clear() # Set screen to white
    # Set scaled top part of the screen to blue
    display.set_pen(BLUE)
    display.rectangle(0, 0, 240, int(drk_rng/5))
    # Set scaled bottom part of screen to red
    display.set_pen(RED)
    display.rectangle(0, int(240-(brt_rng/5)), 240, int(brt_rng/5))
    
    #Set up screen labels
    display.set_pen(BLACK)
    display.text("1300", 5, 0, 240, 1) # top of screen bounds 1300
    display.text(str(too_dark), 5, int(drk_rng/5), 240, 1) # too dark = 1000
    display.text("700", 5, 116, 240, 1)
    display.text(str(too_bright), 5, int(233-(brt_rng/5)), 240, 1) # too bright = 400
    display.text("100", 5, 230, 240, 1) # bottom of screen bounds 100
    
    # On-screen text readout
    display.text(value, 20, 10, 240, 5)
    
    # Update dict to prevent it exceeding 49 elements
    if tick>47:
        for key in list(tick_read_dict.keys()):
            if tick-(key/5)>48:
                del tick_read_dict[key]
    print("length of tick-read_dict: ", len(tick_read_dict))
    
    # Output updating read out values onto screen as plot
    for key, val in tick_read_dict.items():
        display.rectangle(240+key-(tick*5), val, 5, 5)
    display.update()
    
    # Buzzer control
    if ldr.read_u16() > too_dark:
        buzz.set_tone(200) # low buzzing tone for too dark
    else:
        if ldr.read_u16() < too_bright:
            buzz.set_tone(500) # high buzzing tone for too bright
        else:
            buzz.set_tone(0) # stop buzzer when light levels return to acceptable
    
    # Speed Control - Seconds per update
    time.sleep(1)
