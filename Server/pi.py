import time
from datetime import datetime

import RPi.GPIO as GPIO

from lcd import LCD
from thermometer import temp_loop

lcd_loop_flag = True
temp_loop_flag = True


# Pi class stores data for the pi itself, as well as the status variables
# for the button and switch. It holds the lcd object which is created in
# the constructor. The phone messaging information is stored as well as
# the max and min temperature values. It also contains the functions for
# the button and switch interrupts as well as the temp and lcd loops.
class Pi:
    # Constructor for Pi class
    def __init__(self, ip: str, port: int, button_pin: int, switch_pin: int, sensor_id: str):
        self.ip: str = ip  # pi ip address
        self.port: int = port  # pi port
        self.lcd: LCD = LCD()  # lcd object
        self.temp_data: list[int | str] = ["null"] * 300  # temperature data array

        self.switch_status: bool = True  # switch status
        self.button_status_phys: bool = False  # physical button status
        self.button_status_comp: bool = False  # computer button status
        self.button_pin: int = button_pin  # GPIO button pin
        self.switch_pin: int = switch_pin  # GPIO switch pin
        self.sensor_id: str = sensor_id  # GPIO sensor id

        self.message_buffer: bool = False  # message buffer
        self.phone_number: int | None = None  # phone number
        self.carrier: str | None = None  # carrier
        self.min_temp: int = 10  # min temp
        self.max_temp: int = 50  # max temp

        # Set up GPIO pins and settings
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_pin, GPIO.BOTH, callback=self.button_interrupt, bouncetime=20)
        GPIO.setup(self.switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.switch_pin, GPIO.BOTH, callback=self.switch_interrupt, bouncetime=500)

        if GPIO.input(self.switch_pin) == GPIO.LOW:
            self.switch_status = True
            print("Setting To On")
        elif GPIO.input(self.switch_pin) == GPIO.HIGH:
            self.switch_status = False
            print("Setting Off")

    # Function for button interrupt
    def button_interrupt(self, channel):
        print("Button Interrupt!")
        time.sleep(.01)

        # Wait for the button to be released
        if GPIO.input(self.button_pin) == GPIO.LOW:
            self.button_status_phys = True
        elif GPIO.input(self.button_pin) == GPIO.HIGH:
            self.button_status_phys = False

    # Function for switch interrupt
    def switch_interrupt(self, channel):
        print("Switch interrupt")
        time.sleep(.01)

        if GPIO.input(self.switch_pin) == GPIO.LOW:
            self.switch_status = True
            print("Setting To On")
        elif GPIO.input(self.switch_pin) == GPIO.HIGH:
            self.switch_status = False
            print("Setting Off")

    # Function for temperature loop which grabs the current temperature every second
    def run_temp_loop(self):
        while temp_loop_flag:
            start_time = datetime.now()
            temp_loop(self)
            try:
                time.sleep(1 - (datetime.now() - start_time).total_seconds())
            except Exception as e:
                pass

    # Function for LCD loop which constantly checks the switch status and
    # both button statuses to determine what should be displayed on the LCD
    def lcd_loop(self):
        if self.switch_status:
            if self.button_status_phys or self.button_status_comp:
                self.lcd.LCD_BACKLIGHT = 0x08
                self.lcd.message("Temperature:", 1)
                if isinstance(self.temp_data[-1], float):
                    # turn on LCD and display current temperature
                    self.lcd.message(f"{round(self.temp_data[-1], 2)}ßC", 2)
                else:
                    # turn on LCD and display "No Temp Data"
                    self.lcd.message("No Temp Data", 2)
            else:
                # turn off LCD
                self.lcd.LCD_BACKLIGHT = 0x00
                self.lcd.clear()
        else:
            # turn off LCD
            self.lcd.LCD_BACKLIGHT = 0x00
            self.lcd.clear()

    # Function continuously calls lcd_loop
    def run_lcd_loop(self):
        while lcd_loop_flag:
            self.lcd_loop()
