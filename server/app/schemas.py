"""Request/response models. Field names are the wire contract (v1)."""
from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field, field_validator

CAMERA_ID = r"^[a-z0-9][a-z0-9_-]{1,31}$"
ROBOT_ID = r"^[a-z0-9][a-z0-9_-]{1,31}$"

CameraRole = Literal["head_left", "head_right", "arm", "other"]
CommandKind = Literal["stop", "move", "look", "greet", "idle", "calibrate",
                      "follow", "hold", "say", "nose_extend", "nose_retract",
                      "scan", "recon", "report", "pause"]


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


class MissionEventIn(BaseModel):
    type: str = Field(min_length=2, max_length=32)
    data: dict[str, Any] = {}


class MissionOut(BaseModel):
    robot_id: str
    state: str
    started_at: float | None = None
    updated_at: float | None = None
    context: dict[str, Any] = {}
    estopped: bool = False


class ScanOut(BaseModel):
    accepted: bool
    reason: str
    kind: str | None = None
    label: str | None = None
    hits: int = 0
    mean_score: float | None = None
    window_s: float


class DeviceEvent(BaseModel):
    type: str = Field(min_length=2, max_length=24)
    data: dict[str, Any] = {}


class DeviceAck(BaseModel):
    id: int
    ok: bool = True
    note: str | None = Field(default=None, max_length=120)


class DeviceSyncIn(BaseModel):
    """Tek turda durum bildirimi + komut alma (ESP8266 dostu)."""

    ts: float | None = None
    role: Literal["robot", "pentest", "camera", "other"] | None = None
    capabilities: list[str] = Field(default_factory=list, max_length=16)
    rssi: int | None = Field(default=None, ge=-120, le=0)
    battery_v: float | None = Field(default=None, ge=0, le=30)
    firmware: str | None = Field(default=None, max_length=40)
    sensors: dict[str, float] = {}
    activity: str | None = Field(default=None, max_length=64,
                                 description="Şu an ne yapıyor: idle, scanning 10.0.0.5, wifi_scan…")
    progress: float | None = Field(default=None, ge=0, le=1,
                                   description="Aktif işin tamamlanma oranı 0..1")
    events: list[DeviceEvent] = Field(default_factory=list, max_length=8)
    ack: list[DeviceAck] = Field(default_factory=list, max_length=8)


class DeviceCommandOut(BaseModel):
    id: int
    kind: str
    params: dict[str, Any] = {}


class DeviceSyncOut(BaseModel):
    server_time: float
    robot_id: str
    next_poll_s: float
    commands: list[DeviceCommandOut]
    config: dict[str, Any]
    events_applied: int = 0
    acks_applied: int = 0




class FindingIn(BaseModel):
    target: str = Field(min_length=1, max_length=190)
    title: str = Field(min_length=3, max_length=200)
    severity: Literal["info", "low", "medium", "high", "critical"] = "info"
    scan_id: str | None = Field(default=None, max_length=48)
    port: int | None = Field(default=None, ge=0, le=65535)
    proto: str | None = Field(default=None, max_length=12)
    service: str | None = Field(default=None, max_length=48)
    version: str | None = Field(default=None, max_length=64)
    evidence: str | None = Field(default=None, max_length=2000)
    cvss: float | None = Field(default=None, ge=0, le=10)


class FindingOut(FindingIn):
    id: int
    device_id: str
    ts: float
    in_scope: bool


class FindingsIn(BaseModel):
    items: list[FindingIn] = Field(min_length=1, max_length=200)


class DeviceInfoOut(BaseModel):
    id: str
    last_seen: float | None = None
    ip: str | None = None
    rssi: int | None = None
    battery_v: float | None = None
    firmware: str | None = None
    sensors: dict[str, Any] = {}
    sync_count: int = 0
    online: bool = False
    role: str = "robot"
    capabilities: list[str] = []
    activity: str | None = None
    progress: float | None = None
    activity_at: float | None = None
