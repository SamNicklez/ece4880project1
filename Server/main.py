import threading
import time
from datetime import datetime

import RPi.GPIO as GPIO

from apis import app, ButtonAPI, TemperatureAPI
from thermometer import temp_loop


class Pi:
    def __init__(self, ip, port, button_pin, sensor_id):
        self.ip = ip
        self.port = port
        self.temp_data = []
        self.switch_status = True
        self.button_status_phys = False
        self.button_status_comp = False
        self.button_pin = button_pin
        self.sensor_id = sensor_id

        self.phone_number = None
        self.carrier = None
        self.min_temp = None
        self.max_temp = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_pin, GPIO.FALLING, callback=self.button_interrupt, bouncetime=200)

    def button_interrupt(self, channel):
        print("Button pressed!")

        # Wait for the button to be released
        while GPIO.input(self.button_pin) == GPIO.LOW:
            # Push the Temperatures to the LCD
            print("Current Temperature: " + str(self.temp_data[len(self.temp_data) - 1]))
            pass

        print("Button released!")
        # Put your interrupt function code here...

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
                pass
            else:
                # turn off LCD
                pass
        else:
            # turn off LCD
            pass
        pass

    def run_lcd_loop(self):
        while True:
            self.lcd_loop()


def main():
    pi = Pi("0.0.0.0", 5000, 17, '28-3ce0e381d163')

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
