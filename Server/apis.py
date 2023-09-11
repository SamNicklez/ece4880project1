from flask import Flask
from flask.views import MethodView

app = Flask(__name__)

class API(MethodView):
    def __init__(self, pi):
        self.pi = pi
    
    def get(self):
        return str(self.pi.get_temp_data())

    def post(self, status):
        self.pi.set_button_status(status)
        return "Button status set to " + str(status)
    

       