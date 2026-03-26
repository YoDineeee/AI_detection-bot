import time

class FaceTracker:
    def __init__(self, stability_frames: int = 5, cooldown_seconds: float = 15.0):
        self.stability_frames = stability_frames
        self.cooldown_seconds = cooldown_seconds
        self._stable_count = 0
        self._state = "ABSENT"
        self._last_trigger_time = 0.0

    def update(self, face_present: bool) -> bool:
        now = time.time()

        if face_present:
            self._stable_count += 1
        else:
            self._stable_count = 0

        if self._stable_count < self.stability_frames:
            return False

        if now - self._last_trigger_time < self.cooldown_seconds:
            return False

        if self._state == "ABSENT":
            self._state = "PRESENT"
            self._last_trigger_time = now
            return True

        return False

    def notify_absence(self, face_present: bool) -> None:
        if not face_present:
            self._state = "ABSENT"