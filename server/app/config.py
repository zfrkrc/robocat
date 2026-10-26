"""Runtime configuration (env driven, no secrets in code)."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


def _env_float(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    db_path: Path
    frames_dir: Path

    max_frame_bytes: int
    frame_retention: int
    jpeg_quality: int

    detect_width: int
    detector: str  # "hog" | "none" | "yolo"
    yolo_onnx: str
    aruco_dict: str
    aruco_enabled: bool

    command_ttl_s: int
    telemetry_retention: int

    @property
    def version(self) -> str:
        return "0.1.0"


def load_settings() -> Settings:
    data_dir = Path(os.environ.get("ROBO_DATA_DIR", "data")).resolve()
    db_path = Path(os.environ.get("ROBO_DB_PATH", str(data_dir / "robocat.db")))
    frames_dir = Path(os.environ.get("ROBO_FRAMES_DIR", str(data_dir / "frames")))
    data_dir.mkdir(parents=True, exist_ok=True)
    frames_dir.mkdir(parents=True, exist_ok=True)
    return Settings(
        data_dir=data_dir,
        db_path=db_path,
        frames_dir=frames_dir,
        max_frame_bytes=_env_int("ROBO_MAX_FRAME_BYTES", 4 * 1024 * 1024),
        frame_retention=_env_int("ROBO_FRAME_RETENTION", 200),
        jpeg_quality=_env_int("ROBO_JPEG_QUALITY", 80),
        detect_width=_env_int("ROBO_DETECT_WIDTH", 320),
        detector=os.environ.get("ROBO_DETECTOR", "hog").lower(),
        yolo_onnx=os.environ.get("ROBO_YOLO_ONNX", ""),
        aruco_dict=os.environ.get("ROBO_ARUCO_DICT", "DICT_4X4_50"),
        aruco_enabled=os.environ.get("ROBO_ARUCO", "1") not in ("0", "false", "False"),
        command_ttl_s=_env_int("ROBO_COMMAND_TTL_S", 30),
        telemetry_retention=_env_int("ROBO_TELEMETRY_RETENTION", 5000),
    )


settings = load_settings()
