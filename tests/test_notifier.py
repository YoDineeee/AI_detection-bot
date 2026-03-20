import pytest
from unittest.mock import AsyncMock, patch
from src.emotion_bot.notifier import TelegramNotifier


@pytest.fixture
def notifier():
    return TelegramNotifier()


def test_notify_emotion_contains_emotion(notifier):
    with patch.object(notifier._bot, "send_message",
                      new_callable=AsyncMock) as mock_send:
        notifier.notify_emotion("angry", 92.5, "2026-01-01T12:00:00")

        mock_send.assert_called_once()
        text = mock_send.call_args[1]["text"]
        assert "angry"  in text
        assert "92.5"   in text
        assert "😠"     in text


def test_notify_emotion_happy_emoji(notifier):
    with patch.object(notifier._bot, "send_message",
                      new_callable=AsyncMock) as mock_send:
        notifier.notify_emotion("happy", 88.0, "2026-01-01T12:00:00")

        text = mock_send.call_args[1]["text"]
        assert "😊" in text


def test_notify_broker_health_online(notifier):
    with patch.object(notifier._bot, "send_message",
                      new_callable=AsyncMock) as mock_send:
        notifier.notify_broker_health("online")

        text = mock_send.call_args[1]["text"]
        assert "✅" in text


def test_notify_broker_health_offline(notifier):
    with patch.object(notifier._bot, "send_message",
                      new_callable=AsyncMock) as mock_send:
        notifier.notify_broker_health("offline")

        text = mock_send.call_args[1]["text"]
        assert "🔴" in text