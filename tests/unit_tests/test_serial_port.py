import mock
import pytest
from pytest_mock import mocker
from unittest.mock import ANY
#from boom.serial_port import SerialPort


import serial
class SerialPort:
    def __init__(self, port = "/dev/ttyACM0", baudrate = 115200, timeout = 0):
        self.serialPort = serial.Serial(port, baudrate, timeout)

    def read(self, bytesToRead = 1):
        self.serialPort.read(bytesToRead)


@mock.patch("serial.Serial")
class TestSerialPort_Open():
    def test_opens_specified_port(self, mocker):
        port = "/dev/nisse"
        spr = SerialPort(port)
        serial.Serial.assert_called_once_with(port, ANY, ANY)
        
    def test_opens_ttyACM0_by_default(self, mocker):
        spr = SerialPort()
        serial.Serial.assert_called_once_with("/dev/ttyACM0", ANY, ANY)

    def test_opens_baud_115200_by_default(self, mocker):
        spr = SerialPort()
        serial.Serial.assert_called_once_with(ANY, 115200, ANY)

    def test_opens_with_specified_baud(self, mocker):
        baud = 9600
        spr = SerialPort("name", 9600)
        serial.Serial.assert_called_once_with(ANY, baud, ANY)

    def test_opens_with_default_timeout_0(self, mocker):
        spr = SerialPort()
        serial.Serial.assert_called_once_with(ANY, ANY, 0)

    def test_opens_with_specified_timeout(self, mocker):
        timeout = 100
        spr = SerialPort("name", 123, timeout)
        serial.Serial.assert_called_once_with(ANY, ANY, timeout)

# TODO: The following tests are very bad tests since they knows about the serialPort member of SerialPort
# Mock object should be injected instead I suppose


@mock.patch("serial.Serial")
class TestSerialPort_Read():
    @pytest.fixture
    def mocked_serial_port(self, mocker):
        port = SerialPort()
        mocker.patch.object(port.serialPort, "read")
        return port

    def test_read_one_byte_by_default(self, mocker):
        port = self.mocked_serial_port(mocker)
        port.read()
        port.serialPort.read.assert_called_once_with(1)

    def test_read_specified_number_of_bytes(self, mocker):
        port = self.mocked_serial_port(mocker)
        port.read(1000)
        port.serialPort.read.assert_called_once_with(1000)