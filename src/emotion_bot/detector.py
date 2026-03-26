from dataclasses import dataclass
from typing import Optional
import numpy as np
import cv2
from deepface import DeepFace

@dataclass
class DetectionResult:
    emotion: str
    confidence: float
    face_found: bool

class EmotionDetector:
    def detect(self, frame: np.ndarray) -> Optional[DetectionResult]:
        try:
            # Preprocessing for better lighting and accuracy
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_eq = cv2.equalizeHist(gray)
            enhanced = cv2.cvtColor(gray_eq, cv2.COLOR_GRAY2BGR)

            results = DeepFace.analyze(
                enhanced,
                actions=["emotion"],
                enforce_detection=False,
                silent=True,
                detector_backend="retinaface"
            )

            if not results:
                return DetectionResult(
                    emotion="unknown",
                    confidence=0.0,
                    face_found=False
                )

            top = results[0]
            emotion = top["dominant_emotion"]
            confidence = top["emotion"][emotion]

            return DetectionResult(
                emotion=emotion,
                confidence=round(confidence, 2),
                face_found=True
            )

        except Exception as e:
            print(f"[Detector] Error: {e}")
            return None