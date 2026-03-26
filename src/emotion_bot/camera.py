import cv2
from typing import Optional
import numpy as np

class Camera:
    def __init__(self, index: int = 0) -> None:
        self._index = index
        self._cap: Optional[cv2.VideoCapture] = None

    def open(self) -> None:
        self._cap = cv2.VideoCapture(self._index)
        if not self._cap.isOpened():
            raise RuntimeError(f"Cannot open camera at index {self._index}")

    def read(self) -> Optional[np.ndarray]:
        if self._cap is None:
            return None
        ret, frame = self._cap.read()
        return frame if ret else None

    def close(self) -> None:
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    def __enter__(self) -> "Camera":
        self.open()
        return self

    def __exit__(self, *args) -> None:
        self.close()