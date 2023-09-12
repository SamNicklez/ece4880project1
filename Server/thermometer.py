
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