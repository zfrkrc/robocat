"""Frame analysis: quality metrics, ArUco markers, motion/person detection.

Honest scope
------------
* ``motion`` uses MOG2 background subtraction. It reports *moving regions*,
  not people. It is the default because no detector weights are bundled.
* ``yolo`` loads an ONNX model from ``ROBO_YOLO_ONNX`` and keeps class 0
  (person) boxes only. The integration is untested until a model exists.
* ArUco markers give stable, measurable targets; prefer them for
  localisation and calibration instead of "person recognition".
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

import cv2
import numpy as np

from .config import settings


@dataclass
class Detection:
    kind: str
    label: str
    score: float
    box: tuple[float, float, float, float] | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "label": self.label,
            "score": round(float(self.score), 4),
            "box": list(self.box) if self.box else None,
            "extra": self.extra,
        }


class Analyzer:
    def __init__(self) -> None:
        self._motion: Any = None
        self._yolo: Any = None
        self._aruco: Any = None
        self._aruco_dict: Any = None
        self.detector = settings.detector
        self.detector_note = ""

        if settings.aruco_enabled:
            try:
                dict_id = getattr(cv2.aruco, settings.aruco_dict, cv2.aruco.DICT_4X4_50)
                self._aruco_dict = cv2.aruco.getPredefinedDictionary(dict_id)
                self._aruco = cv2.aruco.ArucoDetector(
                    self._aruco_dict, cv2.aruco.DetectorParameters()
                )
            except Exception as exc:  # pragma: no cover - depends on build
                self._aruco = None
                self.detector_note += f"aruco disabled ({exc}); "

        if self.detector == "yolo":
            self._yolo = self._load_yolo(settings.yolo_onnx)
            if self._yolo is None:
                self.detector = "motion"
                self.detector_note += "yolo model missing/unreadable, fell back to motion; "
        if self.detector == "motion":
            self._motion = cv2.createBackgroundSubtractorMOG2(
                history=250, varThreshold=24, detectShadows=False
            )
        if self.detector not in ("motion", "yolo", "none"):
            self.detector = "none"

    # -- model loading -------------------------------------------------
    @staticmethod
    def _load_yolo(path: str) -> Any:
        if not path:
            return None
        try:
            return cv2.dnn.readNetFromONNX(path)
        except Exception:
            return None

    # -- public API ----------------------------------------------------
    def analyze(self, jpeg: bytes) -> dict[str, Any]:
        arr = np.frombuffer(jpeg, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("frame is not a decodable JPEG/PNG image")
        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        brightness = float(gray.mean())
        sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())

        dets: list[Detection] = []
        dets += self._detect_aruco(gray)
        dets += self._detect_people(img)

        return {
            "width": w,
            "height": h,
            "brightness": round(brightness, 2),
            "sharpness": round(sharpness, 2),
            "detector": self.detector,
            "detections": dets,
        }

    # -- detectors -----------------------------------------------------
    def _detect_aruco(self, gray: np.ndarray) -> list[Detection]:
        if self._aruco is None:
            return []
        try:
            corners, ids, _ = self._aruco.detectMarkers(gray)
        except Exception:
            return []
        out: list[Detection] = []
        if ids is None:
            return out
        for idx, marker in enumerate(ids.flatten().tolist()):
            pts = corners[idx][0]
            xs, ys = pts[:, 0], pts[:, 1]
            x0, y0 = float(xs.min()), float(ys.min())
            bw, bh = float(xs.max() - x0), float(ys.max() - y0)
            side = (math.hypot(*(pts[1] - pts[0])) + math.hypot(*(pts[2] - pts[1]))) / 2.0
            out.append(
                Detection(
                    kind="aruco",
                    label=f"marker_{int(marker)}",
                    score=1.0,
                    box=(x0, y0, bw, bh),
                    extra={"marker_id": int(marker), "side_px": round(side, 1)},
                )
            )
        return out

    def _detect_people(self, img: np.ndarray) -> list[Detection]:
        if self.detector == "yolo":
            return self._detect_yolo(img)
        if self.detector == "motion":
            return self._detect_motion(img)
        return []

    def _detect_motion(self, img: np.ndarray) -> list[Detection]:
        h, w = img.shape[:2]
        scale = settings.detect_width / max(w, 1)
        small = cv2.resize(img, (settings.detect_width, max(int(h * scale), 1))) if scale < 1 else img
        fg = self._motion.apply(small)
        fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        fg = cv2.dilate(fg, np.ones((5, 5), np.uint8), iterations=2)
        contours, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        out: list[Detection] = []
        min_area = 0.004 * small.shape[0] * small.shape[1]
        k = 1.0 / max(scale, 1e-6)
        for c in contours:
            area = cv2.contourArea(c)
            if area < min_area:
                continue
            x, y, bw, bh = cv2.boundingRect(c)
            out.append(
                Detection(
                    kind="motion",
                    label="moving_region",
                    score=min(1.0, area / (small.shape[0] * small.shape[1]) * 8),
                    box=(x * k, y * k, bw * k, bh * k),
                    extra={"area_px": round(area * k * k, 1)},
                )
            )
        out.sort(key=lambda d: -(d.box[2] * d.box[3] if d.box else 0))
        return out[:8]

    def _detect_yolo(self, img: np.ndarray) -> list[Detection]:
        if self._yolo is None:
            return []
        try:
            h, w = img.shape[:2]
            blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (640, 640), swapRB=True, crop=False)
            self._yolo.setInput(blob)
            out = self._yolo.forward()
            preds = np.squeeze(out)
            if preds.ndim != 2:
                return []
            if preds.shape[0] < preds.shape[1]:  # (84, N) -> (N, 84)
                preds = preds.T
            boxes, scores = [], []
            sx, sy = w / 640.0, h / 640.0
            for row in preds:
                cls_scores = row[4:]
                if cls_scores.size == 0:
                    continue
                cid = int(cls_scores.argmax())
                score = float(cls_scores[cid])
                if cid != 0 or score < 0.35:
                    continue
                cx, cy, bw, bh = row[0] * sx, row[1] * sy, row[2] * sx, row[3] * sy
                boxes.append([int(cx - bw / 2), int(cy - bh / 2), int(bw), int(bh)])
                scores.append(score)
            if not boxes:
                return []
            keep = cv2.dnn.NMSBoxes(boxes, scores, 0.35, 0.45)
            dets = []
            for i in np.array(keep).flatten().tolist():
                x, y, bw, bh = boxes[i]
                dets.append(Detection("person", "person", scores[i], (float(x), float(y), float(bw), float(bh))))
            return dets[:8]
        except Exception:
            return []


analyzer = Analyzer()
