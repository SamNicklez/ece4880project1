def temp_loop(pi):
    temperature = read_temperature(pi)

    if len(pi.temp_data) >= 300:
        pi.temp_data.pop(0)

    if temperature is None:
        print("ERROR")
    elif temperature == 0.0:
        pi.temp_data.append(False)
    else:
        pi.temp_data.append(temperature)

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
        temperature_line = lines[1].strip().split("=")[-1]
        temperature_celsius = float(temperature_line) / 1000.0

        return temperature_celsius

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
