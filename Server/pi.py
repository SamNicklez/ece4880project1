import time
from datetime import datetime

import RPi.GPIO as GPIO

from lcd import LCD
from thermometer import temp_loop

lcd_loop_flag = True
temp_loop_flag = True


class Pi:
    def __init__(self, ip: str, port: int, button_pin: int, switch_pin: int, sensor_id: str):
        self.ip: str = ip
        self.port: int = port
        self.lcd: LCD = LCD()
        self.temp_data: list[int | str] = ["null"] * 300

        self.switch_status: bool = True
        self.button_status_phys: bool = False
        self.button_status_comp: bool = False
        self.button_pin: int = button_pin
        self.switch_pin: int = switch_pin
        self.sensor_id: str = sensor_id

        self.message_buffer: bool = False
        self.phone_number: int | None = None
        self.carrier: str | None = None
        self.min_temp: int = 10
        self.max_temp: int = 50

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

    def button_interrupt(self, channel):
        print("Button Interrupt!")
        time.sleep(.01)

        # Wait for the button to be released
        if GPIO.input(self.button_pin) == GPIO.LOW:
            self.button_status_phys = True
        elif GPIO.input(self.button_pin) == GPIO.HIGH:
            self.button_status_phys = False

    def switch_interrupt(self, channel):
        print("Switch interrupt")
        time.sleep(.01)

        if GPIO.input(self.switch_pin) == GPIO.LOW:
            self.switch_status = True
            print("Setting To On")
        elif GPIO.input(self.switch_pin) == GPIO.HIGH:
            self.switch_status = False
            print("Setting Off")

    def run_temp_loop(self):
        while temp_loop_flag:
            start_time = datetime.now()
            temp_loop(self)
            try:
                time.sleep(1 - (datetime.now() - start_time).total_seconds())
            except Exception as e:
                pass

    def lcd_loop(self):
        if self.switch_status:
            if self.button_status_phys or self.button_status_comp:
                # turn on LCD
                # display temp
                self.lcd.LCD_BACKLIGHT = 0x08
                self.lcd.message("Temperature:", 1)
                #print("BEFORE LCD LOOP: " + f"{round(self.temp_data[-1], 2)}ßC")
                if isinstance(self.temp_data[-1], float):
                    self.lcd.message(f"{round(self.temp_data[-1], 2)}ßC", 2)
                else:
                    self.lcd.message("No Temp Data", 2)
            else:
                # turn off LCD
                self.lcd.LCD_BACKLIGHT = 0x00
                self.lcd.clear()
        else:
            # turn off LCD
            self.lcd.LCD_BACKLIGHT = 0x00
            self.lcd.clear()

    def run_lcd_loop(self):
        while lcd_loop_flag:
            self.lcd_loop()
