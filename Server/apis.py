from flask import Flask
from flask.views import MethodView

app = Flask(__name__)


class API(MethodView):
    def __init__(self, pi):
        self.pi = pi

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
