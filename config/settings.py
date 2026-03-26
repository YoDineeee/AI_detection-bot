import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Camera
    CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", 0))
    CAMERA_ID = os.getenv("CAMERA_ID", "cam-default")
    DETECTION_INTERVAL = float(os.getenv("DETECTION_INTERVAL", 0.25))

    # MQTT Broker
    BROKER_HOST = os.getenv("BROKER_HOST", "localhost")
    BROKER_PORT = int(os.getenv("BROKER_PORT", 1883))
    BROKER_USERNAME = os.getenv("BROKER_USERNAME")
    BROKER_PASSWORD = os.getenv("BROKER_PASSWORD")

    TOPIC_EMOTIONS = os.getenv("TOPIC_EMOTIONS", "emotions/events")
    TOPIC_HEALTH = os.getenv("TOPIC_HEALTH", "emotions/health")

    # Telegram
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    def validate(self):
        required = ["TELEGRAM_TOKEN", "TELEGRAM_CHAT_ID"]
        for key in required:
            if not getattr(self, key):
                raise ValueError(f"Missing required setting: {key}")

settings = Settings()
settings.validate()