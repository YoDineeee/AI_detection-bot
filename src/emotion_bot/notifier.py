#sends telegram messages
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

async def _send(self, text: str ) -> None:
    try:
        await self._bot.send_message(chat_id = self._chat_id, text =text)
    except  TelegramError as e:
          print(f"[Notifier] Failed to send: {e}")

     
     
 def notify_emotion(self, emotion: str,
                       confidence: float,
                       timestamp: str) -> None:
        emoji = EMOTION_EMOJI.get(emotion, "❓")
        text  = (
            f"{emoji} Emotion Detected\n"
            f"Emotion:    {emotion}\n"
            f"Confidence: {confidence:.1f}%\n"
            f"Time:       {timestamp}"
        )
        asyncio.run(self._send(text))

    def notify_broker_health(self, status: str) -> None:
        icon = "✅" if "online" in status or "running" in status else "🔴"
        asyncio.run(self._send(f"{icon} Broker: {status}"))