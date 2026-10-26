"""Single background worker that turns stored frames into detections.

A thread + queue is enough for three cameras; no broker is required. The
ingest endpoint can also run the analysis inline (``?sync=1``) for tests
and for low frame rates.
"""
from __future__ import annotations

import queue
import threading
from pathlib import Path

from . import db
from .config import settings
from .vision import analyzer

_q: "queue.Queue[tuple[int, str, str]]" = queue.Queue(maxsize=256)
_started = threading.Event()
_lock = threading.Lock()
_stats = {"processed": 0, "failed": 0, "dropped": 0, "last_error": ""}


def _process(frame_id: int, camera_id: str, path: str) -> None:
    data = Path(path).read_bytes()
    result = analyzer.analyze(data)
    db.update_frame_meta(frame_id, result["width"], result["height"],
                         result["brightness"], result["sharpness"])
    for det in result["detections"]:
        db.insert_detection(frame_id, camera_id, det.kind, det.label, det.score, det.box, det.extra)


def _run() -> None:
    while True:
        try:
            frame_id, camera_id, path = _q.get(timeout=1.0)
        except queue.Empty:
            continue
        try:
            _process(frame_id, camera_id, path)
            with _lock:
                _stats["processed"] += 1
        except Exception as exc:  # keep the worker alive, report the cause
            with _lock:
                _stats["failed"] += 1
                _stats["last_error"] = f"{type(exc).__name__}: {exc}"
        finally:
            _q.task_done()
            pairs = db.frames_for_cleanup(camera_id, settings.frame_retention)
            db.delete_frames(pairs)


def start() -> None:
    if _started.is_set():
        return
    with _lock:
        if _started.is_set():
            return
        t = threading.Thread(target=_run, name="vision-worker", daemon=True)
        t.start()
        _started.set()


def submit(frame_id: int, camera_id: str, path: str) -> bool:
    """Queue a frame; returns False when the queue is full (frame is kept)."""
    try:
        _q.put_nowait((frame_id, camera_id, path))
        return True
    except queue.Full:
        with _lock:
            _stats["dropped"] += 1
        return False


def analyze_inline(frame_id: int, camera_id: str, path: str) -> dict:
    result = analyzer.analyze(Path(path).read_bytes())
    db.update_frame_meta(frame_id, result["width"], result["height"],
                         result["brightness"], result["sharpness"])
    for det in result["detections"]:
        db.insert_detection(frame_id, camera_id, det.kind, det.label, det.score, det.box, det.extra)
    return {
        "width": result["width"],
        "height": result["height"],
        "brightness": result["brightness"],
        "sharpness": result["sharpness"],
        "detector": result["detector"],
        "detections": [d.as_dict() for d in result["detections"]],
    }


def stats() -> dict:
    with _lock:
        s = dict(_stats)
    s["queued"] = _q.qsize()
    s["detector"] = analyzer.detector
    s["detector_note"] = analyzer.detector_note.strip()
    return s
