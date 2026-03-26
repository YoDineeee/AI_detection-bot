import signal
import time
from datetime import datetime, timezone
from config.settings import settings

from src.emotion_bot.camera import Camera
from src.emotion_bot.detector import EmotionDetector
from src.emotion_bot.publisher import MqttPublisher
from src.emotion_bot.subscriber import MqttSubscriber
from src.emotion_bot.notifier import TelegramNotifier
from src.emotion_bot.tracker import FaceTracker

class Pipeline:
    def __init__(self) -> None:
        self._camera = Camera(settings.CAMERA_INDEX)
        self._detector = EmotionDetector()
        self._publisher = MqttPublisher()
        self._notifier = TelegramNotifier()
        self._subscriber = MqttSubscriber(
            on_emotion=self._notifier.notify_emotion,
            on_broker_health=self._notifier.notify_broker_health,
        )
        self._tracker = FaceTracker(stability_frames=5, cooldown_seconds=15.0)
        self._running = False
        self._last_frame = None

    def run(self) -> None:
        signal.signal(signal.SIGINT, self._handle_stop)
        signal.signal(signal.SIGTERM, self._handle_stop)

        self._running = True

        with self._camera, self._publisher, self._subscriber:
            self._publisher.publish_health("online")
            print("[Pipeline] Running -- press Ctrl+C to stop")

            while self._running:
                frame = self._camera.read()
                if frame is None:
                    time.sleep(1.0)
                    continue

                self._last_frame = frame.copy()

                result = self._detector.detect(frame)
                face_detected = bool(result and result.face_found)

                should_trigger = self._tracker.update(face_detected)

                if should_trigger and result is not None and self._last_frame is not None:
                    emotion = result.emotion
                    confidence = result.confidence

                    print(f"[Pipeline] TRIGGER → {emotion} ({confidence:.1f}%)")

                    event = {
                        "event": "face_entered",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "camera": getattr(settings, 'CAMERA_ID', "cam-default"),
                        "emotion": emotion,
                        "confidence": round(float(confidence) / 100.0, 3)
                    }

                    self._publisher.publish_face_event(event)

                    self._notifier.notify_emotion_with_image(
                        emotion=emotion,
                        confidence=confidence,
                        timestamp=event["timestamp"],
                        frame=self._last_frame
                    )

                self._tracker.notify_absence(face_detected)
                time.sleep(settings.DETECTION_INTERVAL)

            self._publisher.publish_health("offline")

    def _handle_stop(self, *args) -> None:
        print("\n[Pipeline] Stopping...")
        self._running = False