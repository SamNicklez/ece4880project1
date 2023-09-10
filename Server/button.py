# GPIO can be installed with RPi.GPIO
import RPi.GPIO as GPIO

def check_pin():
    GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
    pin_number = 7  # Change this to your desired pin

    GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set pin to be an input pin and set initial value to be pulled high (on)

    if GPIO.input(pin_number) == GPIO.LOW:  # Check if the pin goes low
        return True
    else:
        return False