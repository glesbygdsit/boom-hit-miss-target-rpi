import mock
import pytest
import requests
import datetime
from pytest_mock import mocker
from unittest.mock import ANY
from boom.serial_port import SerialPort
from boom.poster import Poster

PostAddress = "http://target.zapto.org/hit-miss-target-service"
TargetId = "1337"

@pytest.fixture
def poster():
    return Poster(PostAddress, TargetId)

@mock.patch("requests.post")
class TestPostHit():
    def test_sends_http_post_request(self, mocker):
        poster().post_hit(0)
        requests.post.assert_called_once()

    def test_sends_http_post_to_correct_address(self, mocker):
        poster().post_hit(0)
        requests.post.assert_called_once_with(PostAddress, json=ANY)

    def test_sends_hit_message_with_target_i(self, mocker):
        poster().post_hit(0)
        jsonData = requests.post.call_args[1]["json"]
        assert jsonData["event"] == "vibration_triggered"

    def test_sends_hit_message_with_target_type_hit_miss_target(self, mocker):
        poster().post_hit(0)
        jsonData = requests.post.call_args[1]["json"]
        assert jsonData["target_type"] == "hit_miss_target"

    def test_sends_hit_message_with_target_id(self, mocker):
        poster().post_hit(0)
        jsonData = requests.post.call_args[1]["json"]
        assert jsonData["target_id"] == TargetId

    def test_sends_hit_message_with_vibration_factor_0(self, mocker):
        poster().post_hit(0)
        jsonData = requests.post.call_args[1]["json"]
        assert jsonData["vibration_factor"] == 0.0

    def test_sends_hit_message_with_vibration_factor_1(self, mocker):
        poster().post_hit(1)
        jsonData = requests.post.call_args[1]["json"]
        assert jsonData["vibration_factor"] == 1.0

    def test_sends_hit_message_with_generic_vibration_factor(self, mocker):
        poster().post_hit(0.1337)
        jsonData = requests.post.call_args[1]["json"]
        assert jsonData["vibration_factor"] == 0.1337

    
    def test_sends_hit_message_with_current_time(self, mocker):
        fakeTime = datetime.datetime(2018, 2, 24, 13, 37, 45)
        class FakeDate(datetime.datetime):
            @classmethod
            def now(cls):
                return fakeTime
        datetime.datetime = FakeDate

        poster().post_hit(0)
        jsonData = requests.post.call_args[1]["json"]
        assert jsonData["timestamp"] == "2018-02-24 13:37:45"
