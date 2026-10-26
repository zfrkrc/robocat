import os, sys, tempfile
from pathlib import Path

TMP = Path(tempfile.mkdtemp(prefix="robocat-test-"))
os.environ["ROBO_DATA_DIR"] = str(TMP)
os.environ["ROBO_DETECTOR"] = "motion"
os.environ["ROBO_FRAME_RETENTION"] = "10"
os.environ["ROBO_ENV_CHECK_S"] = "9999"
os.environ["ROBO_ANSWER_TIMEOUT_S"] = "1"
os.environ["ROBO_SENSOR_TIMEOUT_S"] = "1"
os.environ["ROBO_SCAN_TIMEOUT_S"] = "1"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient

@pytest.fixture(scope="session")
def client():
    from app.main import app
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="session")
def jpeg_factory():
    from PIL import Image, ImageDraw
    import io
    def make(marker=None):
        img = Image.new("RGB", (320, 240), (30, 30, 30))
        d = ImageDraw.Draw(img)
        d.rectangle([10, 10, 80, 40], fill=(90, 90, 90))
        if marker:
            d.rectangle(marker, fill=(240, 240, 240))
        b = io.BytesIO(); img.save(b, format="JPEG", quality=85)
        return b.getvalue()

    return make

@pytest.fixture(scope="session")
def aruco_factory():
    import cv2, numpy as np
    def make_aruco(marker_id=7):
        img = np.full((320, 240), 200, dtype=np.uint8)
        d = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        m = cv2.aruco.generateImageMarker(d, marker_id, 140)
        img[50:190, 50:190] = m
        ok, buf = cv2.imencode(".jpg", img)
        assert ok
        return buf.tobytes()
    return make_aruco
