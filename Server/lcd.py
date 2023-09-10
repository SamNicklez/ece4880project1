# This is just example starter code from cursor 
# Install with pip install RPi_I2C_driver

import RPi_I2C_driver
from time import *

mylcd = RPi_I2C_driver.lcd()

try:
    while True:
        mylcd.lcd_display_string("Hello, world!", 1)  # Display string on line 1
        sleep(2)  # Wait for 2 sec
        mylcd.lcd_clear()  # Clear the LCD
        sleep(2)  # Wait for 2 sec
except KeyboardInterrupt:
    print("Cleaning up!")
    mylcd.lcd_clear()