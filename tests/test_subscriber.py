import json
import pytest
from unittest.mock import MagicMock
from src.emotion_bot.subscriber import MqttSubscriber


@pytest.fixture
def subscriber():
    return MqttSubscriber(
        on_emotion       = MagicMock(),
        on_broker_health = MagicMock()
    )


def make_msg(topic: str, payload: dict):
    msg         = MagicMock()
    msg.topic   = topic
    msg.payload = json.dumps(payload).encode()
    return msg


def test_emotion_message_routed(subscriber):
    msg = make_msg("emotions/detection", {
        "emotion": "happy", "confidence": 95.0, "timestamp": "2026-01-01"
    })
    subscriber._on_message(None, None, msg)
    subscriber._on_emotion.assert_called_once_with("happy", 95.0, "2026-01-01")


def test_broker_health_message_routed(subscriber):
    msg = make_msg("$SYS/health/status", {"status": "running"})
    subscriber._on_message(None, None, msg)
    subscriber._on_broker_health.assert_called_once_with("running")


def test_invalid_json_ignored(subscriber):
    msg         = MagicMock()
    msg.topic   = "emotions/detection"
    msg.payload = b"not json"

    subscriber._on_message(None, None, msg)

    subscriber._on_emotion.assert_not_called()


def test_unknown_topic_ignored(subscriber):
    msg = make_msg("some/random/topic", {"data": "value"})
    subscriber._on_message(None, None, msg)

    subscriber._on_emotion.assert_not_called()
    subscriber._on_broker_health.assert_not_called()