from fastapi import FastAPI

app = FastAPI()

@app.get("/past")
async def past():
    # get past 300 sec of data and return it
    pass


@app.get("/current")
async def current():
    # get current data and return it
    pass


@app.post("/activate/{status}")
async def activate():
    # set the LCD to the input status (bool)
    pass

def start_server():
    # start the server
    pass
