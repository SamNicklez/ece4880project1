import os
import time
import RPi.GPIO as GPIO

# Replace <SENSOR_UNIQUE_ID> with your DS18B20 sensor's unique ID
sensor_id = '28-3ce0e381d163'
button_pin = 17

tempValues = []

switchOn = True


def button_interrupt(channel):
    print("Button pressed!")

    # Wait for the button to be released
    while GPIO.input(button_pin) == GPIO.LOW:
        # Push the Temperatures to the LCD
        print("Current Temperature: " + str(tempValues[len(tempValues) - 1]))
        pass

    print("Button released!")
    # Put your interrupt function code here...


GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_interrupt, bouncetime=200)


def read_temperature():
    try:
        # Read the raw temperature data from the sensor
        with open(f"/sys/bus/w1/devices/{sensor_id}/w1_slave", "r") as sensor_file:
            lines = sensor_file.readlines()

        # Extract the temperature from the second line of the output
        temperature_line = lines[1].strip().split("=")[-1]
        temperature_celsius = float(temperature_line) / 1000.0

        return temperature_celsius

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


if __name__ == "__main__":

    # read from the switch to see if it is on or off

    while True:
        temperature = read_temperature()

        if len(tempValues) >= 300:
            tempValues.pop(0)

        if temperature is None:
            print("ERROR")
        elif temperature == 0.0:
            tempValues.append(False)
        else:
            tempValues.append(temperature)

        # print("Temperature: " + str(tempValues) + " °C\n")
        print("Length of Queue: " + str(len(tempValues)))
        time.sleep(1)  # Wait for 1 second before the next reading


