import time
from lcd import LCD

lcd = LCD() # params available for rPi revision, I2C Address, and backlight on/off
            # lcd = LCD(2, 0x3F, True)

lcd.message("Hello World!", 1) # display 'Hello World!' on line 1 of LCD
lcd.message("Yessir", 2)

time.sleep(5) # wait 5 seconds

lcd.clear() # clear LCD display