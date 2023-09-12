from flask import Flask
from flask.views import MethodView

app = Flask(__name__)


class API(MethodView):
    def __init__(self, pi):
        self.pi = pi

    def get(self):
        return str(self.pi.temp_data)

    def post(self, status):
        self.pi.button_status_comp = status
        return "Button status set to " + str(status)
