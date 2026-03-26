import json
import time
from typing import Callable
import paho.mqtt.client as mqtt
from config.settings import settings

class MqttSubscriber:
    def __init__(
        self,
        on_emotion: Callable[[str, float, str], None],
        on_broker_health: Callable[[str], None]
    ) -> None:
        self._on_emotion = on_emotion
        self._on_broker_health = on_broker_health
        self._client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self._connected = False

    def connect(self) -> None:
        if settings.BROKER_USERNAME and settings.BROKER_PASSWORD:
            self._client.username_pw_set(settings.BROKER_USERNAME, settings.BROKER_PASSWORD)

        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message

        self._client.connect(settings.BROKER_HOST, settings.BROKER_PORT)
        self._client.loop_start()

        timeout = 5.0
        start = time.time()
        while not self._connected and time.time() - start < timeout:
            time.sleep(0.1)

        if not self._connected:
            raise RuntimeError("Could not connect to MQTT broker")

    def disconnect(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()

    def _on_connect(self, client, userdata, flags, rc, properties=None) -> None:
        if rc == 0:
            self._connected = True
            client.subscribe(settings.TOPIC_EMOTIONS, qos=1)
            client.subscribe(settings.TOPIC_HEALTH, qos=0)
            print("[Subscriber] Connected and subscribed")

    def _on_disconnect(self, client, userdata, flags, rc, properties=None) -> None:
        self._connected = False

    def _on_message(self, client, userdata, msg) -> None:
        try:
            payload = json.loads(msg.payload.decode())
        except Exception:
            return

        if msg.topic == settings.TOPIC_EMOTIONS:
            emotion = payload.get("emotion", "unknown")
            confidence = payload.get("confidence", 0.0)
            timestamp = payload.get("timestamp", "")
            self._on_emotion(emotion, confidence, timestamp)

        elif msg.topic == settings.TOPIC_HEALTH:
            status = payload.get("status", "unknown")
            self._on_broker_health(status)

    def __enter__(self) -> "MqttSubscriber":
        self.connect()
        return self

    def __exit__(self, *args) -> None:
        self.disconnect()