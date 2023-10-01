from textMessage import send_message


# Function temp_loop continuously reads the temperature from the
# sensor and appends it to the pi's temperature data array
def temp_loop(pi):
    # Read the temperature from the sensor
    try:
        temperature = read_temperature(pi)
    except OSError:
        temperature = None

    # If the temperature data array's length is 300, remove the oldest element
    if len(pi.temp_data) >= 300:
        pi.temp_data.pop(0)

    # Append null if the temperature is None, otherwise append the temperature
    if temperature is None:
        pi.temp_data.append("null")
    else:
        pi.temp_data.append(temperature)

        # Check if the message buffer is False if so a text message can be sent so the current temp is
        # checked against the max and min temp and if it is outside the range a message is sent and the
        # message buffer is set to True. If the message buffer is initially True that means a text has
        # already been sent. The current temperature is then checked against the max and min temp and if
        # it is within the range the message buffer is set to False so a text can be sent again.
        if not pi.message_buffer:
            if temperature > pi.max_temp:
                print("SENDING MAX TEMP MESSAGE")
                message = "MAX TEMP MESSAGE"
                send_message(pi.phone_number, pi.carrier, message)
                pi.message_buffer = True
            elif temperature < pi.min_temp:
                print("SENDING MIN TEMP MESSAGE")
                message = "MIN TEMP MESSAGE"
                send_message(pi.phone_number, pi.carrier, message)
                pi.message_buffer = True
        elif pi.min_temp < temperature < pi.max_temp:
            print("RESET MESSAGE BUFFER")
            pi.message_buffer = False

        print("Temperature: " + str(round(temperature, 2)) + " °C")
        print("Length of Queue: " + str(len(pi.temp_data)))
        print("Switch Status: " + str(pi.switch_status))
        print("Button Status PHYS: " + str(pi.button_status_phys))
        print("Button Status COMP: " + str(pi.button_status_comp))


# Function read_temperature reads the raw temperature data from
# the sensor and returns the temperature in Celsius
def read_temperature(pi):
    try:
        # Read the raw temperature data from the sensor
        with open(f"/sys/bus/w1/devices/{pi.sensor_id}/w1_slave", "r") as sensor_file:
            lines = sensor_file.readlines()

        # Extract the temperature from the second line of the output
        if len(lines) == 0:
            return None
        else:
            temperature_line = lines[1].strip().split("=")[-1]
            temperature_celsius = float(temperature_line) / 1000.0
            return temperature_celsius

    except Exception as e:
        print(f"An error occurred: {str(e)}")
