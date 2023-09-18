import time
from datetime import datetime

import RPi.GPIO as GPIO

from thermometer import temp_loop
from lcd import *

class Pi:
    def __init__(self, ip, port, button_pin, sensor_id):
        self.ip: int = ip
        self.port: int = port
        self.lcd: LCD = LCD()
        self.temp_data: list = ["null"] * 300
        self.switch_status: bool = True
        self.button_status_phys: bool = False
        self.button_status_comp: bool = False
        self.button_pin: int = button_pin
        self.sensor_id: str = sensor_id

        self.message_buffer: bool = False
        self.phone_number: int = None
        self.carrier: str = None
        self.min_temp: int = 10
        self.max_temp: int = 50

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_pin, GPIO.BOTH, callback=self.button_interrupt, bouncetime=20)

    def button_interrupt(self, channel):
        print("Button Interrupt!")
        time.sleep(.01)

        # Wait for the button to be released
        if GPIO.input(self.button_pin) == GPIO.LOW:
            self.button_status_phys = True
        elif GPIO.input(self.button_pin) == GPIO.HIGH:
            self.button_status_phys = False

    def run_temp_loop(self):
        while True:
            a = datetime.now()
            temp_loop(self)
            try:
                time.sleep(1 - (datetime.now() - a).total_seconds())
            except:
                pass

    def lcd_loop(self):
        if self.switch_status:
            if self.button_status_phys or self.button_status_comp:
                # turn on LCD
                # display temp
                self.lcd.LCD_BACKLIGHT = 0x08
                self.lcd.message("Temperature", 1)
                self.lcd.message(f"{self.temp_data[-1]}", 2)
            else:
                # turn off LCD
                self.lcd.LCD_BACKLIGHT = 0x00
                self.lcd.clear()
                
        else:
            # turn off LCD
            self.lcd.LCD_BACKLIGHT = 0x00
            self.lcd.clear()

    def run_lcd_loop(self):
        while True:
            self.lcd_loop()