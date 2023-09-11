from fastapi import FastAPI

from main import Pi

app = FastAPI()


class API:
    def __init__(self, pi: Pi):
        self.pi: Pi = pi

    @app.get("/data")
    async def data(self):
        # get past 300 sec of data and return it
        return self.pi.get_temp_data()

    @app.post("/button/{status}")
    async def button(self, status: bool):
        # set the LCD to the input status (bool)
        self.pi.set_button_status(status)
