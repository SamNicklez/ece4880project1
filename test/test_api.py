import json
from json import JSONDecodeError
import pytest

import sys
import os

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("../Server"))

from Server.main import app, return_response, return_error


# Flask client for mock
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
        
# Mock the Pi object
@pytest.fixture
def mock_pi(mocker):
    mock = mocker.MagicMock()
    mocker.patch('Server.main.pi', mock)
    return mock


# Test for valid POST /button/True
def test_post_button_true(client):
    response = client.post("/button/True")
    assert response.status_code == 200
    assert b"Button status set to True" in response.data


# Test for valid POST /button/False
def test_post_button_false(client):
    response = client.post("/button/False")
    assert response.status_code == 200
    assert b"Button status set to False" in response.data


# Test for invalid POST /button/invalid_status
def test_post_button_invalid(client):
    response = client.post("/button/invalid_status")
    assert response.status_code == 400
    assert b"Invalid Input Status" in response.data


test_input = [
    (1234567890, "att", 100, 0),
    (1234567890, "verizon", 100, 0),
    (1234567890, "uscellular", 100, 0),
    (4984320987, "att", 100, 0),
    (3498561986, "att", 100, 0),
    (1234567890, "att", 50, 0),
    (1234567890, "att", 100, 50),
    (1234567890, "att", 100, -50),
    (1234567890, "att", -50, -100),
]


# Test for valid POST /settings
@pytest.mark.parametrize("phone_number,carrier,max_temp,min_temp", test_input)
def test_post_settings_valid(client, phone_number, carrier, max_temp, min_temp):
    payload = {
        "phone_number": phone_number,
        "carrier": carrier,
        "max_temp": max_temp,
        "min_temp": min_temp,
    }
    expected = f"Successfully Set:\n\tPhone Number = {phone_number}\n\tCarrier = {carrier}\n\tMax Temp = {max_temp}\nTemp = {min_temp}"

    response = client.post(
        "/settings", data=json.dumps(payload), headers={"Content-Type": "text/plain"}
    )
    assert response.data.decode("utf8").replace("'", '"') == expected
    assert response.status_code == 200


test_input = [
    (1234567890, "att", 100, None, "Missing Input Parameters"),
    (1234567890, "att", None, 0, "Missing Input Parameters"),
    (1234567890, None, 100, 0, "Missing Input Parameters"),
    (None, "att", 100, 0, "Missing Input Parameters"),
    (1234567890, "att", 0, 100, "Input min_temp > max_temp"),
    (1234567890, "att", -10, 0, "Input min_temp > max_temp"),
    (1234567890, "invalid_carrier", 100, 0, "Invalid Carrier"),
    (1, "att", 100, 0, "Invalid Phone Number"),
    (1342572572457252457, "att", 100, 0, "Invalid Phone Number"),
    (125624, "att", 100, 0, "Invalid Phone Number"),
]


# Test for invalid inputs POST /settings
@pytest.mark.parametrize("phone_number,carrier,max_temp,min_temp,expected", test_input)
def test_post_settings_invalid_inputs(
    client, phone_number, carrier, max_temp, min_temp, expected
):
    payload = {
        "phone_number": phone_number,
        "carrier": carrier,
        "max_temp": max_temp,
        "min_temp": min_temp,
    }
    response = client.post(
        "/settings", data=json.dumps(payload), headers={"Content-Type": "text/plain"}
    )
    assert response.data.decode("utf8").replace("'", '"') == expected
    assert response.status_code == 400


test_input = [
    ({
        "carrier": "att",
        "max_temp": 100,
        "min_temp": 0,
    }),
    ({
        "phone_number": 1234567890,
        "max_temp": 100,
        "min_temp": 0,
    }),
    ({
        "phone_number": 1234567890,
        "carrier": "att",
        "min_temp": 0,
    }   ),
    ({
        "phone_number": 1234567890,
        "carrier": "att",
        "max_temp": 100,
    }),
]

# Test for invalid request POST /settings
@pytest.mark.parametrize("payload", test_input)
def test_post_settings_invalid_request(client, payload):    
    response = client.post(
        "/settings", data=json.dumps(payload), headers={"Content-Type": "text/plain"}
    )
    assert response.status_code == 500
    
# Test for GET /settings
def test_get_settings(client):
    payload = {
        "phone_number": 1234567890,
        "carrier": "verizon",
        "max_temp": 123,
        "min_temp": -123,
    }
    client.post("/settings", data=json.dumps(payload), headers={"Content-Type": "text/plain"})
    
    response = client.get("/settings")
    json_data = json.loads(response.get_data().decode('utf8').replace("'", '"'))
    assert json_data["phone_number"] == "1234567890"
    assert json_data["carrier"] == "verizon"
    assert json_data["max_temp"] == 123
    assert json_data["min_temp"] == -123
    assert response.status_code == 200

test_input = [
    ([123], [123]),
    ([123, 456, 789], [123, 456, 789]),
    (["null", "null", "null"], ["null", "null", "null"]),
    (["null", 123, "null", 456], ["null", 123, "null", 456]),
]

# Test for GET /temp
@pytest.mark.parametrize("temp_data,expected", test_input)
def test_get_temp(client, mocker, mock_pi, temp_data, expected):
    mock_pi.switch_status = True
    mock_pi.temp_data = temp_data
    
    response = client.get("/temp")
    json_data = json.loads(response.get_data().decode('utf8').replace("'", '"'))
    assert json_data == expected
    assert response.status_code == 200
    

# Test for GET /temp when switch is off
def test_get_temp_switch_off(client, mocker, mock_pi):
    mock_pi.switch_status = False
    
    response = client.get("/temp")
    assert response.data.decode("utf8").replace("'", '"') == "Switch is off"
    assert response.status_code == 403


test_input = [
    ("mock response", 200),
    ("mock response", 201),
    ("mock response", 400),
    ("mock response", 403),
]

# Test for return_response function
@pytest.mark.parametrize("message,status", test_input)
def test_return_response(message, status):
    actual = return_response(message, status)
    
    assert actual.get_data().decode('utf8').replace("'", '"') == message
    assert actual.status_code == status


test_input = [
    (Exception("Exception"), "Exception"),
    (TypeError("TypeError"), "TypeError"),
    (MemoryError("MemoryError"), "MemoryError"),
    (SyntaxError("SyntaxError"), "SyntaxError"),
]

# Test for return_error function
@pytest.mark.parametrize("exception,expected", test_input)
def test_return_error(exception, expected):
    actual = return_error(exception)
    
    assert actual.get_data().decode('utf8').replace("'", '"') == f"An error occurred: {expected}"
    assert actual.status_code == 500


if __name__ == "__main__":
    pytest.main()
