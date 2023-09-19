import threading
import json
import re
from flask import *


from lcd import *
from pi import Pi
from textMessage import CARRIERS


app = Flask(__name__)
pi = Pi("172.23.49.73", 5000, 17, 23, '28-3ce0e381d163')


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


@app.route('/settings', methods=['POST'])
def post_settings():
    try:
        data = request.get_data()
        json_data = json.loads(data.decode('utf8').replace("'", '"'))
        
        if json_data["phone_number"] is not None and json_data["carrier"] is not None and json_data["max_temp"] is not None and \
                json_data["min_temp"] is not None:
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


@app.route('/settings', methods=['GET'])
def get_settings():
    try:
        payload = {
                "phone_number": pi.phone_number,
                "carrier": pi.carrier,
                "max_temp": pi.max_temp,
                "min_temp": pi.min_temp,
            }
        return return_response(json.dumps(payload),200)
    except Exception as e:
        return return_error(e)


@app.route('/temp', methods=['GET'])
def get_temp():
    if pi.switch_status:
        return return_response(json.dumps(pi.temp_data), 200)
    else:
        return return_response("Switch is off", 403)

def return_response(response: str, status):
    resp = app.response_class(
        response=response,
        status=status,
        headers=[('Access-Control-Allow-Origin', '*')],
    )
    return resp

def return_error(e: Exception):
    resp = app.response_class(
        response="An error occurred: " + str(e),
        status=500,
        headers=[('Access-Control-Allow-Origin', '*')],
    )
    return resp


def main():
    temp_thread = threading.Thread(target=pi.run_temp_loop)
    temp_thread.daemon = True
    temp_thread.start()

    lcd_thread = threading.Thread(target=pi.run_lcd_loop)
    lcd_thread.daemon = True
    lcd_thread.start()

    app.run(port=pi.port, host=pi.ip, threaded=True, debug=False)


if __name__ == "__main__":
    main()
