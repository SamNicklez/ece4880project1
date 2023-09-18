from flask import Flask, request
from flask.views import MethodView

app = Flask(__name__)


class ButtonAPI(MethodView):
    def __init__(self, pi):
        self.pi = pi

    def post(self, status: bool):
        try:
            self.pi.button_status_comp = status
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


class TemperatureAPI(MethodView):
    def __init__(self, pi):
        self.pi = pi

    def post(self):
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
                self.pi.phone_number = str(json["phone_number"])
                self.pi.carrier = json["carrier"]
                self.pi.max_temp = int(json["max_temp"])
                self.pi.min_temp = int(json["min_temp"])
                resp = app.response_class(
                    response=f"Successfully Set:\n\
                        \tPhone Number = {self.pi.phone_number}\n\
                        \tCarrier = {self.pi.carrier}\n\
                        \tMax Temp = {self.pi.max_temp}\n\
                        \tMin Temp = {self.pi.min_temp}",
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

    def get(self):
        if self.pi.switch_status:
            resp = app.response_class(
                response=str(self.pi.temp_data),
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
