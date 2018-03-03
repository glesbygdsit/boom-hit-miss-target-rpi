import mock
import pytest
import serial
from pytest_mock import mocker
from unittest.mock import ANY
from boom.serial_port import SerialPort

@mock.patch("serial.serial_for_url")
class TestSerialPort_Open():
    def test_opens_specified_port(self, mocker):
        port = "/dev/nisse"
        spr = SerialPort(port)
        serial.serial_for_url.assert_called_once_with(port, baudrate=ANY, timeout=ANY)
        
    def test_opens_ttyACM0_by_default(self, mocker):
        spr = SerialPort()
        serial.serial_for_url.assert_called_once_with("/dev/ttyACM0", baudrate=ANY, timeout=ANY)

    def test_opens_baud_115200_by_default(self, mocker):
        spr = SerialPort()
        serial.serial_for_url.assert_called_once_with(ANY, baudrate=115200, timeout=ANY)

    def test_opens_with_specified_baud(self, mocker):
        baud = 9600
        spr = SerialPort("name", 9600)
        serial.serial_for_url.assert_called_once_with(ANY, baudrate=baud, timeout=ANY)

    def test_opens_with_default_timeout_0(self, mocker):
        spr = SerialPort()
        serial.serial_for_url.assert_called_once_with(ANY, baudrate=ANY, timeout=0)

    def test_opens_with_specified_timeout(self, mocker):
        timeout = 100
        spr = SerialPort("name", 123, timeout)
        serial.serial_for_url.assert_called_once_with(ANY, baudrate=ANY, timeout=timeout)

# TODO: The following tests are very bad tests since they know about the serialPort member of SerialPort
# Mock object should be injected instead I suppose
@pytest.fixture
def mocked_serial_port(mocker):
    port = SerialPort()
    mocker.patch.object(port.serialPort, "read")
    mocker.patch.object(port.serialPort, "write")
    return port

@mock.patch("serial.serial_for_url")
class TestSerialPort_Read():
    

    def test_read_one_byte_by_default(self, mocker):
        port = mocked_serial_port(mocker)
        port.read()
        port.serialPort.read.assert_called_once_with(1)

    def test_read_specified_number_of_bytes(self, mocker):
        port = mocked_serial_port(mocker)
        port.read(1000)
        port.serialPort.read.assert_called_once_with(1000)

    def test_read_returns_what_pyserial_gives(self, mocker):
        port = mocked_serial_port(mocker)
        port.serialPort.read.return_value = b",1234"
        readData = port.read(1000)
        assert readData == b",1234"

@mock.patch("serial.serial_for_url")
class TestSerialPort_Write():
    def test_write_to_serial_port(self, mocker):
        port = mocked_serial_port(mocker)
        port.serialPort.write.return_value = 5
        assert 5 == port.write(b',1234')
        port.serialPort.write.assert_called_once_with(b',1234')
