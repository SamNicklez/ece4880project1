from flask import Flask, request
from flask.views import MethodView

app = Flask(__name__)


class ButtonAPI(MethodView):
    def __init__(self, pi):
        self.pi = pi

    def post(self, status):
        try:
            self.pi.button_status_comp = status
            resp = app.response_class(
                response="Button status set to " + str(status),
                status=200,
            )
            return resp
        except Exception as e:
            resp = app.response_class(
                response="An error occurred: " + str(e),
                status=500,
            )
            return resp


class TemperatureAPI(MethodView):
    def __init__(self, pi):
        self.pi = pi

    def post(self):
        try:
            if request.form["phone_number"] is not None and request.form["carrier"] is not None and request.form["max_temp"] is not None and request.form["min_temp"] is not None:
                self.pi.phone_number = request.form["phone_number"]
                self.pi.carrier = request.form["carrier"]
                self.pi.max_temp = request.form["max_temp"]
                self.pi.min_temp = request.form["min_temp"]
            else:
                resp = app.response_class(
                    response="Invalid parameters",
                    status=400,
                )
                return resp
        except Exception as e:
            resp = app.response_class(
                response="An error occurred: " + str(e),
                status=500,
            )
            return resp


    def get(self):
        if self.pi.switch_status:
            resp = app.response_class(
                response=str(self.pi.temp_data),
                status=200,
            )
            return resp
        else:
            resp = app.response_class(
                response="Switch is off",
                status=409,
            )
            return resp
