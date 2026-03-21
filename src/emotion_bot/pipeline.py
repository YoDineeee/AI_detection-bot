# wires everything together
import signal
import time
from config.settings import settings
from src.emotion_bot.camera      import Camera
from src.emotion_bot.detector    import EmotionDetector
from src.emotion_bot.publisher   import MqttPublisher
from src.emotion_bot.subscriber  import MqttSubscriber
from src.emotion_bot.notifier    import TelegramNotifier

class Pipeline:
    def __init__(self) -> None:
        self._camera     = Camera(settings.CAMERA_INDEX)
        self._detector   = EmotionDetector()
        self._publisher  = MqttPublisher()
        self._notifier   = TelegramNotifier()
        self._subscriber = MqttSubscriber(
            on_emotion       = self._notifier.notify_emotion,
            on_broker_health = self._notifier.notify_broker_health
        )
        self._running = False

    def run(self) -> None:
        signal.signal(signal.SIGINT,  self._handle_stop)
        signal.signal(signal.SIGTERM, self._handle_stop)
        self._running = True

        with self._camera, self._publisher, self._subscriber:
            self._publisher.publish_health("online")
            print("[Pipeline] Running -- press Ctrl+C to stop")

            while self._running:
                frame = self._camera.read()
                if frame is None:
                    print("[Pipeline] No frame -- retrying...")
                    time.sleep(1.0)
                    continue

                result = self._detector.detect(frame)
                if result and result.face_found:
                    print(f"[Pipeline] {result.emotion} ({result.confidence:.1f}%)")
                    self._publisher.publish_emotion(
                        result.emotion,
                        result.confidence
                    )

                time.sleep(settings.DETECTION_INTERVAL)

            self._publisher.publish_health("offline")

    def _handle_stop(self, *args) -> None:
        print("\n[Pipeline] Stopping...")
        self._running = False