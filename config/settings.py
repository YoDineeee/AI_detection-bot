import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BROKER_HOST:    str = os.getenv("BROKER_HOST","localhost")
    BROKER_PORT:    int=int(os.getenv("BROKER_PORT","1883"))
    BROKER_USERNAME:    str=os.getenv("BROKER_USERNAME","admin")
    BROKER_PASSWORD:    str  =os.getenv("BROKER_PASSWORD","admin")
    CAMERA_INDEX:   int = int(os.getenv("CAMERA_INDEX","0"))
    DETECTION_INTERVAL: float = float (os.getenv("DETECTION_INTERVAL","1.0"))
    TOPIC_EMOTIONS:     str   = os.getenv("TOPIC_EMOTIONS", "emotions/detection")
    TOPIC_HEALTH:       str   = os.getenv("TOPIC_HEALTH", "emotions/health")
    BROKER_HEALTH:      str   = os.getenv("BROKER_HEALTH", "$SYS/health/status")
    TELEGRAM_TOKEN:     str   = os.getenv("TELEGRAM_TOKEN", "")
    TELEGRAM_CHAT_ID:   str   = os.getenv("TELEGRAM_CHAT_ID", "")


    settings = Settings()
