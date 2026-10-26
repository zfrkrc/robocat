import os, sys, tempfile
from pathlib import Path

TMP = Path(tempfile.mkdtemp(prefix="robocat-test-"))
os.environ["ROBO_DATA_DIR"] = str(TMP)
os.environ["ROBO_DETECTOR"] = "motion"
os.environ["ROBO_FRAME_RETENTION"] = "10"
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
