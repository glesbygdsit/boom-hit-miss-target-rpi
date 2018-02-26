import mock
import pytest
import os
from pytest_mock import mocker
from unittest.mock import ANY
import boom.config as Config

@mock.patch("os.getenv")
class TestConfig_GetPostAddress():
    def test_environmental_variable_name(self, mocker):
        Config.get_post_address()
        os.getenv.assert_called_once_with("POST_ADDRESS", ANY)

    def test_value_from_env_variable(self, mocker):
        fakeEnvVariable = "http://blargh"
        os.getenv.return_value = fakeEnvVariable
        assert fakeEnvVariable == Config.get_post_address()

    def test_default_value_if_env_doesnt_exist(self, mocker):
        defaultAddr = "http://target.zapto.org/hit-miss-target-service"
        Config.get_post_address()
        os.getenv.assert_called_once_with(ANY, defaultAddr)

@mock.patch("os.getenv")
class TestConfig_GetSerialPortName():
    def test_environmental_variable_name(self, mocker):
        Config.get_serial_port_name()
        os.getenv.assert_called_once_with("SERIAL_PORT_NAME", ANY)

    def test_value(self, mocker):
        fakeName = "nisse"
        os.getenv.return_value = fakeName
        assert fakeName == Config.get_serial_port_name()
    
    def test_default_name(self, mocker):
        defaultName = "/dev/ttyACM0"
        Config.get_serial_port_name()
        os.getenv.assert_called_once_with(ANY, defaultName)