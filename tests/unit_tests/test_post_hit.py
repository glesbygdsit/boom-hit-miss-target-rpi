import mock
import pytest
import requests
from pytest_mock import mocker
from unittest.mock import ANY
from boom.serial_port import SerialPort

def post_hit(hitFactor):
    requests.post("http://addr", data = {})

@mock.patch("requests.post")
class TestPostHit():
    def test_sends_http_post_request(self, mocker):
        post_hit(0)
        requests.post.assert_called_once()