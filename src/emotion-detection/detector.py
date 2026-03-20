#Deepface emotion detection

from dataclasses import dataclass
from trying import Optional
import numpy as np 
from deepface import Deepface

@dataclass
class DetectionResult:
    emotion:    str
    confidence: float
    face_found: bool


class EmotionDetection:
    def detect(self,frame:np.ndarray)-> Optional[DetectionResult]:
        try:
            results = Deepface.analyze(
                frame,
                actions =["emotion"],
                enforce_detection=False,
                silent=True
            )
        if not results:
            return DetectionResult(
                emotion ="unknown",
                confidence = 0.0,
                face_found=False
            )

        top = results[0]
        emotion = top["dominant_emotion"]
        confidence= top["emotion"][emotion]

        return DetectionResult(
            emotion = emotion,
            confidence= round(confidence,2),
            face_found=True
        )
        except Exception as e:
            print(f"[Detector] Error: {e}")
            return None

            

