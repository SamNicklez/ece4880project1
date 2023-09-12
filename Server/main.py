import threading
import time
from datetime import datetime

import RPi.GPIO as GPIO

from thermometer import read_temperature
from apis import app, API


class Pi:
    def __init__(self, switch_status, button_status_phys, button_status_comp, button_pin, sensor_id):
        self.temp_data = []
        self.switch_status = switch_status
        self.button_status_phys = button_status_phys
        self.button_status_comp = button_status_comp
        self.button_pin = button_pin
        self.sensor_id = sensor_id
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


    def temp_loop(self):
        temperature = read_temperature(self)

        if len(self.temp_data) >= 300:
            self.temp_data.pop(0)

        if temperature is None:
            print("ERROR")
        elif temperature == 0.0:
            self.temp_data.append(False)
        else:
            self.temp_data.append(temperature)

        print("Temperature: " + str(temperature) + " °C")
        print("Length of Queue: " + str(len(self.temp_data)))
        print("Switch Status: " + str(self.switch_status))
        print("Button Status PHYS: " + str(self.button_status_phys))
        print("Button Status COMP: " + str(self.button_status_comp))


    def run_temp_loop(self):
        while True:
            a = datetime.now()
            self.temp_loop()
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
    pi = Pi(True, False, 17, '28-3ce0e381d163')
    app.add_url_rule('/data', view_func=API.as_view('data', pi=pi))
    app.add_url_rule('/button/<status>', view_func=API.as_view('button', pi=pi))

    temp_thread = threading.Thread(target=pi.run_temp_loop)
    temp_thread.daemon = True
    temp_thread.start()

    lcd_thread = threading.Thread(target=pi.run_lcd_loop)
    lcd_thread.daemon = True
    lcd_thread.start()

    API(pi)
    app.run(port=5000, host='0.0.0.0')


if __name__ == "__main__":
    main()
