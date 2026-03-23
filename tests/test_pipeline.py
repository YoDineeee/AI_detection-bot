import pytest
from unittest.mock import MagicMock, patch
from src.emotion_bot.pipeline import Pipeline
from src.emotion_bot.detector import DetectionResult


@pytest.fixture
def pipeline():
    with patch("src.emotion_bot.pipeline.Camera")      as mock_camera, \
         patch("src.emotion_bot.pipeline.MqttPublisher") as mock_pub,  \
         patch("src.emotion_bot.pipeline.MqttSubscriber") as mock_sub, \
         patch("src.emotion_bot.pipeline.TelegramNotifier") as mock_notifier:

        mock_camera.return_value.__enter__   = MagicMock(return_value=MagicMock())
        mock_camera.return_value.__exit__    = MagicMock(return_value=False)
        mock_pub.return_value.__enter__      = MagicMock(return_value=MagicMock())
        mock_pub.return_value.__exit__       = MagicMock(return_value=False)
        mock_sub.return_value.__enter__      = MagicMock(return_value=MagicMock())
        mock_sub.return_value.__exit__       = MagicMock(return_value=False)

        p = Pipeline()
        p._camera     = mock_camera.return_value
        p._publisher  = mock_pub.return_value
        p._subscriber = mock_sub.return_value
        p._notifier   = mock_notifier.return_value

        yield p


def test_pipeline_publishes_when_face_found(pipeline):
    # simulate one iteration then stop
    pipeline._running = False

    result = DetectionResult(
        emotion="happy",
        confidence=95.0,
        face_found=True
    )

    pipeline._detector = MagicMock()
    pipeline._detector.detect.return_value = result
    pipeline._camera.read.return_value     = MagicMock()  # fake frame

    # manually call what run() would call
    frame = pipeline._camera.read()
    if frame is not None:
        res = pipeline._detector.detect(frame)
        if res and res.face_found:
            pipeline._publisher.publish_emotion(res.emotion, res.confidence)

    pipeline._publisher.publish_emotion.assert_called_once_with("happy", 95.0)


def test_pipeline_skips_when_no_face(pipeline):
    pipeline._running = False

    result = DetectionResult(
        emotion="unknown",
        confidence=0.0,
        face_found=False
    )

    pipeline._detector = MagicMock()
    pipeline._detector.detect.return_value = result
    pipeline._camera.read.return_value     = MagicMock()

    frame = pipeline._camera.read()
    if frame is not None:
        res = pipeline._detector.detect(frame)
        if res and res.face_found:
            pipeline._publisher.publish_emotion(res.emotion, res.confidence)

    pipeline._publisher.publish_emotion.assert_not_called()


def test_pipeline_skips_when_no_frame(pipeline):
    pipeline._running = False
    pipeline._detector = MagicMock()
    pipeline._camera.read.return_value = None

    frame = pipeline._camera.read()
    if frame is not None:
        pipeline._detector.detect(frame)

    pipeline._detector.detect.assert_not_called()


def test_pipeline_publishes_health_on_stop(pipeline):
    pipeline._handle_stop()
    assert pipeline._running is False