import sys
import time
from unittest.mock import MagicMock, call, patch

import pytest

# Mock smbus and gpio libraries for testing outside of Raspberry Pi
sys.modules["smbus"] = MagicMock()
sys.modules["smbus.SMBus"] = MagicMock()
sys.modules["RPi"] = MagicMock()
sys.modules["RPi.GPIO"] = MagicMock()

from Server import lcd, textMessage

sys.modules["lcd"] = lcd
sys.modules["textMessage"] = textMessage

from Server import thermometer

sys.modules["thermometer"] = thermometer

from Server.pi import Pi
from Server.lcd import LCD


# Test for Pi class constructor
def test_pi_init():
    pi = Pi("mock_ip", 1234, 1, 2, "mock_id")
    assert pi.ip == "mock_ip"
    assert pi.port == 1234
    assert isinstance(pi.lcd, LCD)
    assert pi.temp_data == ["null"] * 300

    assert pi.switch_status is True
    assert pi.button_status_phys is False
    assert pi.button_status_comp is False
    assert pi.button_pin == 1
    assert pi.switch_pin == 2
    assert pi.sensor_id == "mock_id"

    assert pi.message_buffer is False
    assert pi.phone_number is None
    assert pi.carrier is None
    assert pi.min_temp == 10
    assert pi.max_temp == 50


# Test for button_interrupt function
@patch("Server.pi.GPIO.LOW", True)
@patch("Server.pi.GPIO.HIGH", False)
@patch("Server.pi.GPIO.input")
def test_button_interrupt(mock_input):
    pi = Pi("mock_ip", 1234, 1, 2, "mock_id")

    time.sleep = MagicMock(return_value=None)

    mock_input.side_effect = lambda pin_number: {1: True, 2: False}[pin_number]

    pi.button_pin = 1
    pi.button_interrupt(1)
    assert pi.button_status_phys is True

    pi.button_pin = 2
    pi.button_interrupt(1)
    assert pi.button_status_phys is False

    assert time.sleep.call_count == 2


# Test for button_interrupt function
@patch("Server.pi.GPIO.LOW", True)
@patch("Server.pi.GPIO.HIGH", False)
@patch("Server.pi.GPIO.input")
def test_switch_interrupt(mock_input):
    pi = Pi("mock_ip", 1234, 1, 2, "mock_id")

    time.sleep = MagicMock(return_value=None)

    mock_input.side_effect = lambda pin_number: {1: True, 2: False}[pin_number]

    pi.switch_pin = 1
    pi.switch_interrupt(1)
    assert pi.switch_status is True

    pi.switch_pin = 2
    pi.switch_interrupt(1)
    assert pi.switch_status is False

    assert time.sleep.call_count == 2


test_input = [
    (False, False, False, [123], "lcd_off"),
    (False, False, True, [123], "lcd_off"),
    (False, True, False, [123], "lcd_off"),
    (False, True, True, [123], "lcd_off"),
    (True, False, False, [123], "lcd_off"),
    (True, False, True, [123], "lcd_on"),
    (True, True, False, [123], "lcd_on"),
    (True, True, True, [123], "lcd_on"),
    (True, True, True, ["null"], "no_data"),
]


# Test for lcd_loop function
@pytest.mark.parametrize("switch,button_phys,button_comp,temp_data,expected", test_input)
def test_pi_lcd_loop(switch, button_phys, button_comp, temp_data, expected):
    pi = Pi("mock_ip", 1234, 1, 2, "mock_id")

    pi.lcd.message = MagicMock()
    pi.lcd.clear = MagicMock()

    pi.switch_status = switch
    pi.button_status_phys = button_phys
    pi.button_status_comp = button_comp
    pi.temp_data = temp_data
    pi.lcd_loop()

    if expected == "lcd_on":
        assert pi.lcd.LCD_BACKLIGHT == 0x08
        assert pi.lcd.message.call_count == 2
        pi.lcd.message.assert_has_calls([call("Temperature:", 1), call(f"123ßC", 2)])
    elif expected == "lcd_off":
        assert pi.lcd.LCD_BACKLIGHT == 0x00
        pi.lcd.clear.assert_called_once()
