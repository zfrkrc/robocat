"""RoboCat server API v1.

Ingest:
  ESP32-CAM / bridge  -> POST /api/v1/cameras/{camera_id}/frame   (image/jpeg body)
Control:
  robot bridge        -> GET  /api/v1/robots/{robot_id}/commands/next
                         POST /api/v1/robots/{robot_id}/commands/{cmd_id}/ack
  operator            -> POST /api/v1/robots/{robot_id}/commands
                         POST /api/v1/robots/{robot_id}/emergency_stop
Watch:
  browser             -> GET  /api/v1/cameras/{camera_id}/stream.mjpg
                         GET  /api/v1/cameras/{camera_id}/detections
"""
from __future__ import annotations

import hmac
import os
import time
from collections import Counter, defaultdict
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from . import db, mission, pipeline
from .config import settings
from .schemas import (AckIn, CameraIn, CameraOut, CommandIn, CommandOut, DetectionOut,
                      DeviceInfoOut, DeviceSyncIn, DeviceSyncOut, DeviceCommandOut,
                      EmergencyIn, FrameResult, MissionEventIn, MissionOut, ScanOut,
                      TelemetryIn, TelemetryOut)

@asynccontextmanager
async def lifespan(_: FastAPI):
    db.init_db()
    pipeline.start()
    mission.start_ticker()
    yield


app = FastAPI(title="RoboCat server", version=settings.version, lifespan=lifespan,
              description="Camera ingest, vision results, telemetry and command queue.")

_origins = [o for o in os.environ.get("ROBO_CORS_ORIGINS", "*").split(",") if o]
app.add_middleware(CORSMiddleware, allow_origins=_origins, allow_methods=["*"], allow_headers=["*"])

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


def _camera_dir(camera_id: str) -> Path:
    d = settings.frames_dir / camera_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def _camera_known(camera_id: str) -> dict:
    for cam in db.camera_list():
        if cam["id"] == camera_id:
            return cam
    raise HTTPException(404, f"camera '{camera_id}' is not registered")


def _online(cam: dict) -> bool:
    ts = cam.get("last_frame_at")
    return bool(ts) and (time.time() - float(ts) < 5.0)


# ---------------------------------------------------------------- health
@app.get("/api/v1/health")
def health() -> dict:
    return {
        "ok": True,
        "version": settings.version,
        "detector": pipeline.stats(),
        "cameras": len(db.camera_list()),
        "data_dir": str(settings.data_dir),
    }


# --------------------------------------------------------------- cameras
@app.get("/api/v1/cameras", response_model=list[CameraOut])
def cameras_list() -> list[CameraOut]:
    return [CameraOut(**c, online=_online(c)) for c in db.camera_list()]


@app.post("/api/v1/cameras", response_model=CameraOut, status_code=201)
def camera_register(cam: CameraIn) -> CameraOut:
    db.camera_upsert(cam.id, cam.name, cam.role, cam.width, cam.height)
    row = _camera_known(cam.id)
    db.log_event("camera.registered", f"{cam.id} ({cam.role})", camera_id=cam.id)
    return CameraOut(**row, online=_online(row))


@app.post("/api/v1/cameras/{camera_id}/frame", response_model=FrameResult, status_code=202)
async def camera_frame(camera_id: str, request: Request, sync: int = Query(0, ge=0, le=1)) -> FrameResult:
    _camera_known(camera_id)
    body = await request.body()
    if not body:
        raise HTTPException(400, "empty body; send image/jpeg bytes")
    if len(body) > settings.max_frame_bytes:
        raise HTTPException(413, f"frame larger than {settings.max_frame_bytes} bytes")
    if len(body) < 3 or body[:2] != b"\xff\xd8":
        raise HTTPException(415, "expecting JPEG (SOI marker not found)")

    seq = db.next_frame_seq(camera_id)
    path = _camera_dir(camera_id) / f"{seq:08d}.jpg"
    path.write_bytes(body)
    (path.parent / "latest.jpg").write_bytes(body)
    frame_id = db.insert_frame(camera_id, seq, str(path), len(body))

    analysis = None
    queued = False
    if sync:
        analysis = pipeline.analyze_inline(frame_id, camera_id, str(path))
    else:
        queued = pipeline.submit(frame_id, camera_id, str(path))

    return FrameResult(camera_id=camera_id, frame_id=frame_id, seq=seq,
                       ts=time.time(), bytes=len(body), queued=queued, analysis=analysis)


@app.get("/api/v1/cameras/{camera_id}/latest.jpg")
def camera_latest(camera_id: str) -> FileResponse:
    _camera_known(camera_id)
    p = settings.frames_dir / camera_id / "latest.jpg"
    if not p.exists():
        raise HTTPException(404, "no frame received yet")
    return FileResponse(p, media_type="image/jpeg", headers={"Cache-Control": "no-store"})


@app.get("/api/v1/cameras/{camera_id}/stream.mjpg")
def camera_stream(camera_id: str, fps: float = Query(5.0, gt=0.2, le=30)) -> StreamingResponse:
    _camera_known(camera_id)
    latest = settings.frames_dir / camera_id / "latest.jpg"

    def gen():
        period = 1.0 / fps
        while True:
            try:
                data = latest.read_bytes()
            except OSError:
                time.sleep(period)
                continue
            yield (b"--frame\r\nContent-Type: image/jpeg\r\nContent-Length: "
                   + str(len(data)).encode() + b"\r\n\r\n" + data + b"\r\n")
            time.sleep(period)

    return StreamingResponse(gen(), media_type="multipart/x-mixed-replace; boundary=frame")


@app.get("/api/v1/cameras/{camera_id}/detections", response_model=list[DetectionOut])
def camera_detections(camera_id: str, limit: int = Query(50, ge=1, le=500),
                      since: float | None = None) -> list[DetectionOut]:
    _camera_known(camera_id)
    return [DetectionOut(**d) for d in db.detections_recent(camera_id, limit, since)]


@app.get("/api/v1/detections", response_model=list[DetectionOut])
def detections_all(limit: int = Query(50, ge=1, le=500), since: float | None = None) -> list[DetectionOut]:
    return [DetectionOut(**d) for d in db.detections_recent(None, limit, since)]


# -------------------------------------------------------------- telemetry
@app.post("/api/v1/robots/{robot_id}/telemetry", response_model=TelemetryOut, status_code=201)
def telemetry_post(robot_id: str, body: TelemetryIn) -> TelemetryOut:
    tid = db.insert_telemetry(robot_id, body.battery_v, body.current_a, body.imu, body.extra)
    db.telemetry_prune(robot_id, settings.telemetry_retention)
    row = db.telemetry_latest(robot_id)
    if not row:
        raise HTTPException(500, "telemetry write failed")
    return TelemetryOut(**row)


@app.get("/api/v1/robots/{robot_id}/state")
def robot_state(robot_id: str) -> dict:
    latest = db.telemetry_latest(robot_id)
    return {
        "robot_id": robot_id,
        "estopped": db.flags_get(robot_id),
        "telemetry": latest,
        "commands": db.commands_recent(robot_id, limit=10),
    }


# --------------------------------------------------------------- commands
@app.post("/api/v1/robots/{robot_id}/commands", response_model=CommandOut, status_code=201)
def command_create(robot_id: str, body: CommandIn) -> CommandOut:
    if db.flags_get(robot_id) and body.kind != "stop":
        raise HTTPException(409, "emergency stop engaged; only 'stop' is accepted")
    cid = db.command_enqueue(robot_id, body.kind, body.params)
    db.log_event("command.queued", body.kind, robot_id=robot_id)
    return CommandOut(id=cid, robot_id=robot_id, ts=time.time(), kind=body.kind,
                      params=body.params, status="queued")


@app.get("/api/v1/robots/{robot_id}/commands/next", response_model=CommandOut | None)
def command_next(robot_id: str) -> CommandOut | None:
    cmd = db.command_claim_next(robot_id, settings.command_ttl_s)
    return CommandOut(**cmd) if cmd else None


@app.post("/api/v1/robots/{robot_id}/commands/{command_id}/ack")
def command_ack(robot_id: str, command_id: int, body: AckIn) -> dict:
    if not db.command_ack(robot_id, command_id, body.ok, body.note):
        raise HTTPException(404, "command not found or already finished")
    db.log_event("command.ack", f"id={command_id} ok={body.ok}", robot_id=robot_id)
    return {"ok": True, "id": command_id}


@app.get("/api/v1/robots/{robot_id}/commands", response_model=list[CommandOut])
def commands_list(robot_id: str, limit: int = Query(50, ge=1, le=200)) -> list[CommandOut]:
    return [CommandOut(**c) for c in db.commands_recent(robot_id, limit)]


@app.post("/api/v1/robots/{robot_id}/emergency_stop")
def emergency_stop(robot_id: str, body: EmergencyIn) -> dict:
    db.flags_set(robot_id, body.engaged)
    db.log_event("robot.estop", f"engaged={body.engaged} {body.note or ''}".strip(), robot_id=robot_id)
    return {"robot_id": robot_id, "estopped": body.engaged}


# ---------------------------------------------------------------- devices
def _device_keys() -> dict[str, str]:
    """ROBO_DEVICE_KEYS="esp32-1:secret,esp32-2:other" """
    raw = os.environ.get("ROBO_DEVICE_KEYS", "").strip()
    out: dict[str, str] = {}
    for item in raw.split(","):
        if ":" in item:
            did, key = item.split(":", 1)
            if did.strip() and key.strip():
                out[did.strip()] = key.strip()
    return out


def _device_robots() -> dict[str, str]:
    raw = os.environ.get("ROBO_DEVICE_ROBOTS", "").strip()
    out: dict[str, str] = {}
    for item in raw.split(","):
        if ":" in item:
            did, rid = item.split(":", 1)
            if did.strip() and rid.strip():
                out[did.strip()] = rid.strip()
    return out


_last_sync: dict[str, float] = {}
MIN_INTERVAL_S = float(os.environ.get("ROBO_DEVICE_MIN_INTERVAL_S", 0.4))


def _require_device(request: Request, device_id: str) -> None:
    keys = _device_keys()
    presented = request.headers.get("X-Device-Key", "")
    if not keys:
        host = request.client.host if request.client else ""
        if host in ("127.0.0.1", "::1", "testclient"):
            return  # development mode: loopback only
        raise HTTPException(503, "device keys are not configured (ROBO_DEVICE_KEYS)")
    expected = keys.get(device_id)
    if not expected or not hmac.compare_digest(expected, presented):
        raise HTTPException(401, "invalid device key")


@app.post("/api/v1/device/{device_id}/sync", response_model=DeviceSyncOut)
def device_sync(device_id: str, body: DeviceSyncIn, request: Request) -> DeviceSyncOut:
    """Tek tur: durum bildir + komut al. ESP8266 için tasarlandı."""
    _require_device(request, device_id)

    now = time.time()
    last = _last_sync.get(device_id, 0.0)
    if now - last < MIN_INTERVAL_S:
        raise HTTPException(429, f"poll too fast; wait {MIN_INTERVAL_S:.2f}s")
    _last_sync[device_id] = now

    robot_id = _device_robots().get(device_id, device_id)
    ip = request.client.host if request.client else None
    db.device_touch(device_id, ip, body.rssi, body.battery_v, body.firmware, body.sensors)
    if body.battery_v is not None:
        db.insert_telemetry(robot_id, body.battery_v, body.sensors.get("current_a"),
                            {k: v for k, v in body.sensors.items() if k in ("pitch", "roll", "yaw")},
                            {"source": "device", "device_id": device_id, **body.sensors})

    applied_events = 0
    for ev in body.events:
        res = mission.for_robot(robot_id).handle(ev.type, ev.data)
        if res.get("ok") is not False:
            applied_events += 1

    applied_acks = 0
    for a in body.ack:
        if db.command_ack(robot_id, a.id, a.ok, a.note):
            applied_acks += 1

    cmds: list[DeviceCommandOut] = []
    for _ in range(2):  # en fazla 2 komut / tur: ESP8266 tamponu küçük kalsın
        c = db.command_claim_next(robot_id, settings.command_ttl_s)
        if not c:
            break
        cmds.append(DeviceCommandOut(id=c["id"], kind=c["kind"], params=c["params"]))

    return DeviceSyncOut(
        server_time=now,
        robot_id=robot_id,
        next_poll_s=float(os.environ.get("ROBO_DEVICE_POLL_S", 2)),
        commands=cmds,
        config={
            "env_check_s": float(os.environ.get("ROBO_ENV_CHECK_S", 60)),
            "answer_timeout_s": float(os.environ.get("ROBO_ANSWER_TIMEOUT_S", 8)),
            "sensor_timeout_s": float(os.environ.get("ROBO_SENSOR_TIMEOUT_S", 20)),
            "command_ttl_s": settings.command_ttl_s,
        },
        events_applied=applied_events,
        acks_applied=applied_acks,
    )


@app.get("/api/v1/devices", response_model=list[DeviceInfoOut])
def devices_list() -> list[DeviceInfoOut]:
    return [DeviceInfoOut(**d) for d in db.device_list()]


# ---------------------------------------------------------------- mission
def _recognize(camera_id: str, window_s: float, min_hits: int) -> dict:
    """Deterministic decision from stored detections.

    Rules (no randomness):
      * ArUco marker seen in >= min_hits frames -> accepted, identity = marker id.
      * Person detector seen in >= min_hits frames with mean score >= 0.35 -> accepted.
      * Motion alone -> never accepted (it is not identity).
    """
    since = time.time() - window_s
    rows = db.detections_recent(camera_id, limit=400, since=since)
    aruco = Counter()
    person = []
    for d in rows:
        if d["kind"] == "aruco":
            aruco[d["label"]] += 1
        elif d["kind"] == "person":
            person.append(float(d["score"] or 0.0))

    if aruco:
        label, hits = aruco.most_common(1)[0]
        if hits >= min_hits:
            return {"accepted": True, "reason": "aruco_repeated", "kind": "aruco",
                    "label": label, "hits": hits, "mean_score": 1.0, "window_s": window_s}
    if len(person) >= min_hits:
        mean = sum(person) / len(person)
        if mean >= 0.35:
            return {"accepted": True, "reason": "person_repeated", "kind": "person",
                    "label": "person", "hits": len(person), "mean_score": round(mean, 3),
                    "window_s": window_s}
    return {"accepted": False, "reason": "insufficient_evidence",
            "kind": None, "label": None,
            "hits": max([*aruco.values(), len(person)] or [0]),
            "mean_score": None, "window_s": window_s}


@app.post("/api/v1/robots/{robot_id}/mission/start", response_model=MissionOut)
def mission_start(robot_id: str) -> MissionOut:
    mission.for_robot(robot_id).start()
    return MissionOut(**mission.for_robot(robot_id).state())


@app.post("/api/v1/robots/{robot_id}/mission/stop")
def mission_stop(robot_id: str) -> dict:
    return mission.for_robot(robot_id).stop()


@app.get("/api/v1/robots/{robot_id}/mission", response_model=MissionOut)
def mission_state(robot_id: str) -> MissionOut:
    return MissionOut(**mission.for_robot(robot_id).state())


@app.post("/api/v1/robots/{robot_id}/mission/event", response_model=MissionOut)
def mission_event(robot_id: str, body: MissionEventIn) -> MissionOut:
    result = mission.for_robot(robot_id).handle(body.type, body.data)
    if result.get("ok") is False:
        raise HTTPException(409, result.get("error", "event rejected"))
    return MissionOut(**mission.for_robot(robot_id).state())


@app.get("/api/v1/robots/{robot_id}/recognize", response_model=ScanOut)
def recognize(robot_id: str, camera_id: str, window_s: float = Query(3.0, gt=0.2, le=30),
              min_hits: int = Query(2, ge=1, le=20)) -> ScanOut:
    _camera_known(camera_id)
    return ScanOut(**_recognize(camera_id, window_s, min_hits))


@app.post("/api/v1/robots/{robot_id}/mission/scan", response_model=ScanOut)
def mission_scan(robot_id: str, camera_id: str, window_s: float = Query(3.0, gt=0.2, le=30),
                 min_hits: int = Query(2, ge=1, le=20)) -> ScanOut:
    _camera_known(camera_id)
    result = _recognize(camera_id, window_s, min_hits)
    mission.for_robot(robot_id).handle("scan_result", result)
    return ScanOut(**result)


# -------------------------------------------------------------- dashboard
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def dashboard() -> HTMLResponse:
    index = STATIC_DIR / "index.html"
    if index.exists():
        return HTMLResponse(index.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>RoboCat server</h1><p>See /docs for the API.</p>")


@app.get("/favicon.ico")
def favicon() -> Response:
    return Response(status_code=204)
