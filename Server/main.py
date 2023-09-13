import threading
import time
from datetime import datetime

import RPi.GPIO as GPIO

from apis import app, ButtonAPI, TemperatureAPI
from thermometer import temp_loop
from lcd import *


class Pi:
    def __init__(self, ip, port, button_pin, sensor_id):
        self.ip = ip
        self.port = port
        self.lcd = LCD()
        self.temp_data = ["null"] * 300
        self.switch_status = True
        self.button_status_phys = False
        self.button_status_comp = False
        self.button_pin = button_pin
        self.sensor_id = sensor_id

        self.phone_number = None
        self.carrier = None
        self.min_temp = 10
        self.max_temp = 50

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_pin, GPIO.BOTH, callback=self.button_interrupt, bouncetime=20)

    def button_interrupt(self, channel):
        print("Button Interrupt!")
        time.sleep(.01)

        # Wait for the button to be released
        if GPIO.input(self.button_pin) == GPIO.LOW:
            print("LOW")
            self.button_status_phys = True
        elif GPIO.input(self.button_pin) == GPIO.HIGH:
            print("HIGH")
            self.button_status_phys = False

    def run_temp_loop(self):
        while True:
            a = datetime.now()
            temp_loop(self)
            time.sleep(1 - (datetime.now() - a).total_seconds())

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


def main():
    pi = Pi("172.23.49.73", 5000, 17, '28-3ce0e381d163')

    app.add_url_rule('/data', view_func=TemperatureAPI.as_view('data', pi=pi))
    app.add_url_rule('/button/<status>', view_func=ButtonAPI.as_view('button', pi=pi))

    temp_thread = threading.Thread(target=pi.run_temp_loop)
    temp_thread.daemon = True
    temp_thread.start()

    lcd_thread = threading.Thread(target=pi.run_lcd_loop)
    lcd_thread.daemon = True
    lcd_thread.start()

    TemperatureAPI(pi)
    ButtonAPI(pi)

    app.run(port=pi.port, host=pi.ip)


if __name__ == "__main__":
    main()
