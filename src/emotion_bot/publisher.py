
import json
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
from config.settings import settings


class MqttPublisher:
    def __init__(self) -> None:
        self._client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self._connected = False

    def connect(self) -> None:
        self._client.username_pw_set(
            settings.BROKER_USERNAME,
            settings.BROKER_PASSWORD
        )
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.connect(settings.BROKER_HOST, settings.BROKER_PORT)
        self._client.loop_start()

        timeout = 5.0
        start = time.time()
        while not self._connected and time.time() - start < timeout:
            time.sleep(0.1)
        if not self._connected:
            raise RuntimeError("Could not connect to broker")

    def publish_face_event(self, event: dict) -> None:
        payload = json.dumps(event, separators=(",", ":"))  # compact
        self._client.publish(
            topic=settings.TOPIC_EMOTIONS,
            payload=payload,
            qos=1
        )
        print(f"[Publisher] → {settings.TOPIC_EMOTIONS}  ({len(payload)} bytes)")

    def publish_health(self, status: str) -> None:
        payload = json.dumps({
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        self._client.publish(settings.TOPIC_HEALTH, payload, qos=0)

    def disconnect(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()

    def _on_connect(self, client, userdata, flags, rc, properties) -> None:
        self._connected = rc == 0

    def _on_disconnect(self, client, userdata, flags, rc, properties) -> None:
        self._connected = False

    def __enter__(self) -> "MqttPublisher":
        self.connect()
        return self

    def __exit__(self, *args) -> None:
        self.disconnect()