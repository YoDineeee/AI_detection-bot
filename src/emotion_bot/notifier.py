import cv2
import numpy as np
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from config.settings import settings

EMOTION_EMOJI = {
    "happy":    "😊",
    "sad":      "😢",
    "angry":    "😠",
    "fear":     "😨",
    "surprise": "😲",
    "disgust":  "🤢",
    "neutral":  "😐",
    "unknown":  "❓",
}

class TelegramNotifier:
    def __init__(self) -> None:
        self._bot = Bot(token=settings.TELEGRAM_TOKEN)
        self._chat_id = settings.TELEGRAM_CHAT_ID

    async def _send(self, text: str) -> None:
        try:
            await self._bot.send_message(chat_id=self._chat_id, text=text)
        except TelegramError as e:
            print(f"[Notifier] Failed to send message: {e}")

    async def _send_photo(self, image_bytes: bytes, caption: str) -> None:
        try:
            await self._bot.send_photo(
                chat_id=self._chat_id,
                photo=image_bytes,
                caption=caption
            )
        except TelegramError as e:
            print(f"[Notifier] Failed to send photo: {e}")

    def notify_emotion(self, emotion: str, confidence: float, timestamp: str) -> None:
        emoji = EMOTION_EMOJI.get(emotion, "❓")
        text = (
            f"{emoji} Emotion Detected\n"
            f"Emotion:    {emotion}\n"
            f"Confidence: {confidence:.1f}%\n"
            f"Time:       {timestamp}"
        )
        asyncio.run(self._send(text))

    def notify_emotion_with_image(
        self, emotion: str, confidence: float, timestamp: str, frame: np.ndarray
    ) -> None:
        small = cv2.resize(frame, (320, 240))
        _, buffer = cv2.imencode(".jpg", small, [cv2.IMWRITE_JPEG_QUALITY, 75])
        image_bytes = buffer.tobytes()

        emoji = EMOTION_EMOJI.get(emotion, "❓")
        caption = (
            f"{emoji} Emotion Detected\n"
            f"Emotion:    {emotion}\n"
            f"Confidence: {confidence:.1f}%\n"
            f"Time:       {timestamp}"
        )

        asyncio.run(self._send_photo(image_bytes, caption))

    def notify_broker_health(self, status: str) -> None:
        icon = "✅" if any(x in status.lower() for x in ["online", "running"]) else "🔴"
        asyncio.run(self._send(f"{icon} Broker: {status}"))