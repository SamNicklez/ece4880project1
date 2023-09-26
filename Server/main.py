import json
import re
import threading

from flask import *

from pi import Pi
from textMessage import CARRIERS

app = Flask(__name__)
pi = Pi("172.23.49.73", 5000, 17, 23, '28-3ce0e381d163')


# POST /button/<status>
# Input:
#       - status: True or False
# Response:
#       - 200: Button status set to True/False
#       - 400: Invalid Input Status
# Set button_status_comp to input status
@app.route('/button/<status>', methods=['POST'])
def post_button(status: bool):
    try:
        if status == "True":
            pi.button_status_comp = True
            return return_response("Button status set to True", 200)
        elif status == "False":
            pi.button_status_comp = False
            return return_response("Button status set to False", 200)
        else:
            return return_response("Invalid Input Status", 400)
    except Exception as e:
        return return_error(e)


# POST /settings
# Inputs:
#     - request body: {
#           "phone_number": <phone_number>,
#           "carrier": <carrier>,
#           "max_temp": <max_temp>,
#           "min_temp": <min_temp>
#       }
# Response:
#       - 200: Success
#       - 400: Input min_temp > max_temp, Invalid Carrier, Invalid Phone Number, Missing Input Parameters
# Set the Pi's phone number, carrier, max_temp, and min_temp
@app.route('/settings', methods=['POST'])
def post_settings():
    try:
        data = request.get_data()
        json_data = json.loads(data.decode('utf8').replace("'", '"'))

        # Check if all input parameters are present
        if json_data["phone_number"] is not None and json_data["carrier"] is not None and json_data[
            "max_temp"] is not None and \
                json_data["min_temp"] is not None:
            # Check min_temp < max_temp, carrier is valid, and phone number is valid
            if int(json_data["min_temp"]) > int(json_data["max_temp"]):
                return return_response("Input min_temp > max_temp", 400)
            elif json_data["carrier"] not in CARRIERS.keys():
                return return_response("Invalid Carrier", 400)
            elif re.match(r'^\d{10}$', str(json_data["phone_number"])) is None:
                return return_response("Invalid Phone Number", 400)
            else:
                pi.phone_number = str(json_data["phone_number"])
                pi.carrier = json_data["carrier"]
                pi.max_temp = int(json_data["max_temp"])
                pi.min_temp = int(json_data["min_temp"])
                return_message = f"Successfully Set:\n\tPhone Number = {pi.phone_number}\n\tCarrier = {pi.carrier}\n\tMax Temp = {pi.max_temp}\nTemp = {pi.min_temp}"
                return return_response(return_message, 200)
        else:
            return return_response("Missing Input Parameters", 400)
    except Exception as e:
        return return_error(e)


# GET /settings
# Response:
#       - 200: Success
# Get the Pi's phone number, carrier, max_temp, and min_temp
@app.route('/settings', methods=['GET'])
def get_settings():
    try:
        payload = {
            "phone_number": pi.phone_number,
            "carrier": pi.carrier,
            "max_temp": pi.max_temp,
            "min_temp": pi.min_temp,
        }
        return return_response(json.dumps(payload), 200)
    except Exception as e:
        return return_error(e)


# GET /temp
# Response:
#       - 200: Success
#       - 403: Switch is off
# Get the Pi's temperature data
@app.route('/temp', methods=['GET'])
def get_temp():
    # Only send temperature data if switch is on
    if pi.switch_status:
        return return_response(json.dumps(pi.temp_data), 200)
    else:
        return return_response("Switch is off", 403)


# Function return_response takes in a response message
# and a status code and returns a Flask response object
def return_response(response: str, status):
    resp = app.response_class(
        response=response,
        status=status,
        headers=[('Access-Control-Allow-Origin', '*')],
    )
    return resp


# Function return_error takes in an exception and returns
# a Flask response object
def return_error(e: Exception):
    resp = app.response_class(
        response="An error occurred: " + str(e),
        status=500,
        headers=[('Access-Control-Allow-Origin', '*')],
    )
    return resp


# Main function
# Creates two threads for the Pi's continuous temperature and LCD loops
# Runs the Flask app
def main():
    # Thread for continuous temperature loop
    temp_thread = threading.Thread(target=pi.run_temp_loop)
    temp_thread.daemon = True
    temp_thread.start()

    # Thread for continuous LCD loop
    lcd_thread = threading.Thread(target=pi.run_lcd_loop)
    lcd_thread.daemon = True
    lcd_thread.start()

    # Start Flask app
    app.run(port=pi.port, host=pi.ip, threaded=True, debug=False)


if __name__ == "__main__":
    main()
