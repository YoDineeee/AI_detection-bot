import json
import pytest
from unittest.mock import MagicMock, patch
from src.emotion_bot.publisher import MqttPublisher


@pytest.fixture
def publisher():
    pub = MqttPublisher()
    pub._connected = True
    pub._client    = MagicMock()
    return pub


def test_publish_emotion_correct_topic(publisher):
    publisher.publish_emotion("happy", 95.0)

    publisher._client.publish.assert_called_once()
    topic = publisher._client.publish.call_args[0][0]
    assert topic == "emotions/detection"


def test_publish_emotion_correct_payload(publisher):
    publisher.publish_emotion("angry", 88.5)

    payload = json.loads(publisher._client.publish.call_args[0][1])
    assert payload["emotion"]    == "angry"
    assert payload["confidence"] == 88.5
    assert "timestamp" in payload


def test_publish_emotion_qos1(publisher):
    publisher.publish_emotion("sad", 70.0)

    qos = publisher._client.publish.call_args[1].get("qos") or \
          publisher._client.publish.call_args[0][2]
    assert qos == 1


def test_publish_health_online(publisher):
    publisher.publish_health("online")

    payload = json.loads(publisher._client.publish.call_args[0][1])
    assert payload["status"] == "online"