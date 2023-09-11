import time
from datetime import datetime

import RPi.GPIO as GPIO
import apis


class Pi:
    def __init__(self, switch_status, button_status, button_pin, sensor_id):
        self.temp_data = []
        self.switch_status = switch_status
        self.button_status = button_status
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

    def read_temperature(self):
        try:
            # Read the raw temperature data from the sensor
            with open(f"/sys/bus/w1/devices/{self.sensor_id}/w1_slave", "r") as sensor_file:
                lines = sensor_file.readlines()

            # Extract the temperature from the second line of the output
            temperature_line = lines[1].strip().split("=")[-1]
            temperature_celsius = float(temperature_line) / 1000.0

            return temperature_celsius

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def temp_loop(self):
        start_time = datetime.now()
        temperature = self.read_temperature()

        if len(self.temp_data) >= 300:
            self.temp_data.pop(0)

        if temperature is None:
            print("ERROR")
        elif temperature == 0.0:
            self.temp_data.append(False)
        else:
            self.temp_data.append(temperature)

        # print("Temperature: " + str(tempValues) + " °C\n")
        print("Length of Queue: " + str(len(self.temp_data)))
        sleep_time = datetime.now() - start_time
        print(sleep_time)
        time.sleep(sleep_time.total_seconds())


def main():
    pi = Pi(True, False, 17, '28-3ce0e381d163')
    apis.start_server()
    while True:
        pi.temp_loop()


if __name__ == "__main__":
    main()
