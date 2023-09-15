from textMessage import send_message

def temp_loop(pi):
    try:
        temperature = read_temperature(pi)
    except OSError:
        temperature = None

    if len(pi.temp_data) >= 300:
        pi.temp_data.pop(0)

    if temperature is None:
        pi.temp_data.append("null")
    else:
        pi.temp_data.append(temperature)
        
    
    if pi.message_buffer == False:
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

    print("Temperature: " + str(temperature) + " °C")
    print("Length of Queue: " + str(len(pi.temp_data)))
    print("Switch Status: " + str(pi.switch_status))
    print("Button Status PHYS: " + str(pi.button_status_phys))
    print("Button Status COMP: " + str(pi.button_status_comp))


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
        return None
