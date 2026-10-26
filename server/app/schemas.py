"""Request/response models. Field names are the wire contract (v1)."""
from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field, field_validator

CAMERA_ID = r"^[a-z0-9][a-z0-9_-]{1,31}$"
ROBOT_ID = r"^[a-z0-9][a-z0-9_-]{1,31}$"

CameraRole = Literal["head_left", "head_right", "arm", "other"]
CommandKind = Literal["stop", "move", "look", "greet", "idle", "calibrate"]


class CameraIn(BaseModel):
    id: str = Field(pattern=CAMERA_ID)
    name: str = Field(min_length=1, max_length=48)
    role: CameraRole = "other"
    width: int | None = Field(default=None, ge=16, le=4096)
    height: int | None = Field(default=None, ge=16, le=4096)


class CameraOut(CameraIn):
    created_at: float
    last_frame_at: float | None = None
    frames_total: int = 0
    online: bool = False


class DetectionOut(BaseModel):
    id: int | None = None
    frame_id: int | None = None
    camera_id: str
    ts: float
    kind: str
    label: str
    score: float | None = None
    x: float | None = None
    y: float | None = None
    w: float | None = None
    h: float | None = None
    extra: dict[str, Any] = {}


class FrameResult(BaseModel):
    camera_id: str
    frame_id: int
    seq: int
    ts: float
    bytes: int
    queued: bool
    analysis: dict[str, Any] | None = None


class TelemetryIn(BaseModel):
    battery_v: float | None = Field(default=None, ge=0, le=30)
    current_a: float | None = Field(default=None, ge=-60, le=60)
    imu: dict[str, float] = {}
    extra: dict[str, Any] = {}


class TelemetryOut(TelemetryIn):
    id: int
    robot_id: str
    ts: float


class CommandIn(BaseModel):
    kind: CommandKind
    params: dict[str, Any] = {}

    @field_validator("params")
    @classmethod
    def _limit_params(cls, v: dict[str, Any]) -> dict[str, Any]:
        if len(v) > 20:
            raise ValueError("params may contain at most 20 keys")
        return v


class CommandOut(BaseModel):
    id: int
    robot_id: str
    ts: float
    kind: str
    params: dict[str, Any] = {}
    status: str
    claimed_at: float | None = None
    done_at: float | None = None
    note: str | None = None


class AckIn(BaseModel):
    ok: bool = True
    note: str | None = Field(default=None, max_length=200)


class EmergencyIn(BaseModel):
    engaged: bool = True
    note: str | None = Field(default=None, max_length=200)
