import numpy as np
import pytest
from unittest.mock import patch
from src.emotion_bot.detector import EmotionDetector, DetectionResult


@pytest.fixture
def detector():
    return EmotionDetector()


def test_detect_happy_face(detector):
    mock_result = [{
        "dominant_emotion": "happy",
        "emotion": {"happy": 95.0, "sad": 5.0}
    }]

    with patch("src.emotion_bot.detector.DeepFace.analyze",
               return_value=mock_result):
        result = detector.detect(np.zeros((480, 640, 3), dtype=np.uint8))

    assert result is not None
    assert result.emotion    == "happy"
    assert result.confidence == 95.0
    assert result.face_found is True


def test_detect_no_face(detector):
    with patch("src.emotion_bot.detector.DeepFace.analyze",
               return_value=[]):
        result = detector.detect(np.zeros((480, 640, 3), dtype=np.uint8))

    assert result is not None
    assert result.face_found is False
    assert result.emotion    == "unknown"


def test_detect_model_error(detector):
    with patch("src.emotion_bot.detector.DeepFace.analyze",
               side_effect=Exception("model error")):
        result = detector.detect(np.zeros((480, 640, 3), dtype=np.uint8))

    assert result is None


def test_detect_confidence_rounded(detector):
    mock_result = [{
        "dominant_emotion": "angry",
        "emotion": {"angry": 87.3456}
    }]

    with patch("src.emotion_bot.detector.DeepFace.analyze",
               return_value=mock_result):
        result = detector.detect(np.zeros((480, 640, 3), dtype=np.uint8))

    assert result is not None
    assert result.confidence == 87.35
    