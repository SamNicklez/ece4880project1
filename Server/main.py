import threading
import json
from flask import Flask, request

from lcd import *
from pi import Pi


app = Flask(__name__)
pi = Pi("172.23.49.73", 5000, 17, '28-3ce0e381d163')


@app.route('/button/<status>', methods=['POST'])
def post_button(status: bool):
    try:
        pi.button_status_comp = status
        resp = app.response_class(
            response="Button status set to " + str(status),
            status=200,
            headers=[('Access-Control-Allow-Origin', '*')],
        )
        return resp
    except Exception as e:
        resp = app.response_class(
            response="An error occurred: " + str(e),
            status=500,
            headers=[('Access-Control-Allow-Origin', '*')],
        )
        return resp


@app.route('/settings', methods=['POST'])
def post_settings():
    try:
        if request.is_json:
            json = request.get_json()
        else:
            resp = app.response_class(
                response="Invalid JSON",
                status=400,
                headers=[('Access-Control-Allow-Origin', '*')],
            )
            return resp

        if json["phone_number"] is not None and json["carrier"] is not None and json["max_temp"] is not None and \
                json["min_temp"] is not None:
            pi.phone_number = str(json["phone_number"])
            pi.carrier = json["carrier"]
            pi.max_temp = int(json["max_temp"])
            pi.min_temp = int(json["min_temp"])
            resp = app.response_class(
                response=f"Successfully Set:\n\
                    \tPhone Number = {pi.phone_number}\n\
                    \tCarrier = {pi.carrier}\n\
                    \tMax Temp = {pi.max_temp}\n\
                    \tMin Temp = {pi.min_temp}",
                status=200,
                headers=[('Access-Control-Allow-Origin', '*')],
            )
            return resp
        else:
            resp = app.response_class(
                response="Invalid parameters",
                status=400,
                headers=[('Access-Control-Allow-Origin', '*')],
            )
            return resp
    except Exception as e:
        resp = app.response_class(
            response="An error occurred: " + str(e),
            status=500,
            headers=[('Access-Control-Allow-Origin', '*')],
        )
        return resp


@app.route('/settings', methods=['GET'])
def get_settings():
    try:
        resp = app.response_class (
            response={
                "phone_number": pi.phone_number,
                "carrier": pi.carrier,
                "max_temp": pi.max_temp,
                "min_temp": pi.min_temp,
            },
            status=200,
            headers=[('Access-Control-Allow-Origin', '*')],
        )
        return resp
    except Exception as e:
        resp = app.response_class(
            response="An error occurred: " + str(e),
            status=500,
            headers=[('Access-Control-Allow-Origin', '*')],
        )
        return resp


@app.route('/temp', methods=['GET'])
def get_temp():
    if pi.switch_status:
        resp = app.response_class(
            response=json.dumps(pi.temp_data),
            status=200,
            headers=[('Access-Control-Allow-Origin', '*')],
        )
        return resp
    else:
        resp = app.response_class(
            response="Switch is off",
            status=409,
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

    app.run(port=pi.port, host=pi.ip, threaded=True)


if __name__ == "__main__":
    main()
