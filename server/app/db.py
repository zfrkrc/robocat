"""SQLite storage: schema plus small helpers.

One connection per call keeps this dependency-free and safe with the
threaded worker; WAL mode allows the ingest path and the vision worker
to write concurrently.
"""
from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Iterable

from .config import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS cameras (
    id            TEXT PRIMARY KEY,
    name          TEXT NOT NULL,
    role          TEXT NOT NULL,
    width         INTEGER,
    height        INTEGER,
    created_at    REAL NOT NULL,
    last_frame_at REAL,
    frames_total  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS frames (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    camera_id   TEXT NOT NULL,
    seq         INTEGER NOT NULL,
    ts          REAL NOT NULL,
    path        TEXT NOT NULL,
    bytes       INTEGER NOT NULL,
    width       INTEGER,
    height      INTEGER,
    brightness  REAL,
    sharpness   REAL,
    processed   INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_frames_cam_ts ON frames(camera_id, ts DESC);

CREATE TABLE IF NOT EXISTS detections (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    frame_id  INTEGER NOT NULL,
    camera_id TEXT NOT NULL,
    ts        REAL NOT NULL,
    kind      TEXT NOT NULL,
    label     TEXT NOT NULL,
    score     REAL,
    x         REAL, y REAL, w REAL, h REAL,
    extra     TEXT
);
CREATE INDEX IF NOT EXISTS idx_det_cam_ts ON detections(camera_id, ts DESC);

CREATE TABLE IF NOT EXISTS telemetry (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    robot_id  TEXT NOT NULL,
    ts        REAL NOT NULL,
    battery_v REAL,
    current_a REAL,
    imu       TEXT,
    extra     TEXT
);
CREATE INDEX IF NOT EXISTS idx_tel_robot_ts ON telemetry(robot_id, ts DESC);

CREATE TABLE IF NOT EXISTS commands (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    robot_id   TEXT NOT NULL,
    ts         REAL NOT NULL,
    kind       TEXT NOT NULL,
    params     TEXT,
    status     TEXT NOT NULL DEFAULT 'queued',
    claimed_at REAL,
    done_at    REAL,
    note       TEXT
);
CREATE INDEX IF NOT EXISTS idx_cmd_robot_status ON commands(robot_id, status, id);

CREATE TABLE IF NOT EXISTS robot_flags (
    robot_id   TEXT PRIMARY KEY,
    estopped   INTEGER NOT NULL DEFAULT 0,
    updated_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS mission (
    robot_id   TEXT PRIMARY KEY,
    state      TEXT NOT NULL,
    started_at REAL,
    updated_at REAL NOT NULL,
    context    TEXT
);

CREATE TABLE IF NOT EXISTS devices (
    id          TEXT PRIMARY KEY,
    last_seen   REAL,
    ip          TEXT,
    rssi        INTEGER,
    battery_v   REAL,
    firmware    TEXT,
    sensors     TEXT,
    sync_count  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS findings (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id   TEXT NOT NULL,
    scan_id     TEXT,
    ts          REAL NOT NULL,
    target      TEXT NOT NULL,
    port        INTEGER,
    proto       TEXT,
    service     TEXT,
    version     TEXT,
    severity    TEXT,
    title       TEXT NOT NULL,
    evidence    TEXT,
    cvss        REAL,
    in_scope    INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_findings_dev_ts ON findings(device_id, ts DESC);
CREATE INDEX IF NOT EXISTS idx_findings_scan ON findings(scan_id);

CREATE TABLE IF NOT EXISTS events (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    ts        REAL NOT NULL,
    kind      TEXT NOT NULL,
    robot_id  TEXT,
    camera_id TEXT,
    message   TEXT
);
"""


def connect() -> sqlite3.Connection:
    settings.db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(settings.db_path, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def _migrate(conn: sqlite3.Connection) -> None:
    """Küçük, geriye dönük uyumlu şema eklemeleri."""
    cols = {r["name"] for r in conn.execute("PRAGMA table_info(devices)").fetchall()}
    if "role" not in cols:
        conn.execute("ALTER TABLE devices ADD COLUMN role TEXT DEFAULT 'robot'")
    if "capabilities" not in cols:
        conn.execute("ALTER TABLE devices ADD COLUMN capabilities TEXT")
    if "activity" not in cols:
        conn.execute("ALTER TABLE devices ADD COLUMN activity TEXT")
    if "progress" not in cols:
        conn.execute("ALTER TABLE devices ADD COLUMN progress REAL")
    if "activity_at" not in cols:
        conn.execute("ALTER TABLE devices ADD COLUMN activity_at REAL")
    # eski satırları normalize et: NULL rol/yetenek serileştirmeyi bozmasın
    conn.execute("UPDATE devices SET role='robot' WHERE role IS NULL OR role=''")
    conn.execute("UPDATE devices SET capabilities='[]' WHERE capabilities IS NULL OR capabilities=''")


def init_db() -> None:
    with connect() as conn:
        conn.executescript(SCHEMA)
        _migrate(conn)


def log_event(kind: str, message: str, robot_id: str | None = None, camera_id: str | None = None) -> None:
    with connect() as conn:
        conn.execute(
            "INSERT INTO events (ts, kind, robot_id, camera_id, message) VALUES (?,?,?,?,?)",
            (time.time(), kind, robot_id, camera_id, message),
        )


def camera_upsert(camera_id: str, name: str, role: str, width: int | None, height: int | None) -> None:
    now = time.time()
    with connect() as conn:
        conn.execute(
            """INSERT INTO cameras (id, name, role, width, height, created_at)
               VALUES (?,?,?,?,?,?)
               ON CONFLICT(id) DO UPDATE SET
                 name=excluded.name, role=excluded.role,
                 width=COALESCE(excluded.width, cameras.width),
                 height=COALESCE(excluded.height, cameras.height)""",
            (camera_id, name, role, width, height, now),
        )


def camera_list() -> list[dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM cameras ORDER BY role, id"
        ).fetchall()
    return [dict(r) for r in rows]


def next_frame_seq(camera_id: str) -> int:
    with connect() as conn:
        row = conn.execute(
            "SELECT COALESCE(MAX(seq), 0) + 1 AS n FROM frames WHERE camera_id=?", (camera_id,)
        ).fetchone()
        return int(row["n"])


def insert_frame(camera_id: str, seq: int, path: str, size: int) -> int:
    now = time.time()
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO frames (camera_id, seq, ts, path, bytes) VALUES (?,?,?,?,?)",
            (camera_id, seq, now, path, size),
        )
        conn.execute(
            "UPDATE cameras SET last_frame_at=?, frames_total=frames_total+1 WHERE id=?",
            (now, camera_id),
        )
        return int(cur.lastrowid)


def update_frame_meta(frame_id: int, width: int, height: int, brightness: float, sharpness: float) -> None:
    with connect() as conn:
        conn.execute(
            "UPDATE frames SET width=?, height=?, brightness=?, sharpness=?, processed=1 WHERE id=?",
            (width, height, brightness, sharpness, frame_id),
        )


def insert_detection(frame_id: int, camera_id: str, kind: str, label: str, score: float,
                     box: tuple[float, float, float, float] | None, extra: dict | None = None) -> None:
    x, y, w, h = box if box else (None, None, None, None)
    with connect() as conn:
        conn.execute(
            """INSERT INTO detections (frame_id, camera_id, ts, kind, label, score, x, y, w, h, extra)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (frame_id, camera_id, time.time(), kind, label, score, x, y, w, h,
             json.dumps(extra or {}, ensure_ascii=False)),
        )


def detections_recent(camera_id: str | None, limit: int = 50, since: float | None = None) -> list[dict[str, Any]]:
    q = "SELECT * FROM detections"
    where, args = [], []
    if camera_id:
        where.append("camera_id=?"); args.append(camera_id)
    if since:
        where.append("ts>=?"); args.append(since)
    if where:
        q += " WHERE " + " AND ".join(where)
    q += " ORDER BY id DESC LIMIT ?"
    args.append(limit)
    with connect() as conn:
        rows = conn.execute(q, args).fetchall()
    out = []
    for r in rows:
        d = dict(r); d["extra"] = json.loads(d["extra"] or "{}"); out.append(d)
    return out


def insert_telemetry(robot_id: str, battery_v: float | None, current_a: float | None,
                     imu: dict | None, extra: dict | None) -> int:
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO telemetry (robot_id, ts, battery_v, current_a, imu, extra) VALUES (?,?,?,?,?,?)",
            (robot_id, time.time(), battery_v, current_a,
             json.dumps(imu or {}, ensure_ascii=False), json.dumps(extra or {}, ensure_ascii=False)),
        )
        return int(cur.lastrowid)


def telemetry_latest(robot_id: str) -> dict[str, Any] | None:
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM telemetry WHERE robot_id=? ORDER BY id DESC LIMIT 1", (robot_id,)
        ).fetchone()
    if not row:
        return None
    d = dict(row); d["imu"] = json.loads(d["imu"] or "{}"); d["extra"] = json.loads(d["extra"] or "{}")
    return d


def telemetry_prune(robot_id: str, keep: int) -> None:
    with connect() as conn:
        conn.execute(
            """DELETE FROM telemetry WHERE robot_id=? AND id NOT IN
               (SELECT id FROM telemetry WHERE robot_id=? ORDER BY id DESC LIMIT ?)""",
            (robot_id, robot_id, keep),
        )


def mission_get(robot_id: str) -> dict[str, Any] | None:
    with connect() as conn:
        row = conn.execute("SELECT * FROM mission WHERE robot_id=?", (robot_id,)).fetchone()
    if not row:
        return None
    d = dict(row)
    d["context"] = json.loads(d["context"] or "{}")
    return d


def mission_set(robot_id: str, state: str, context: dict | None = None, started_at: float | None = None) -> None:
    now = time.time()
    with connect() as conn:
        cur = conn.execute("SELECT started_at FROM mission WHERE robot_id=?", (robot_id,)).fetchone()
        start = started_at if started_at is not None else (cur["started_at"] if cur else now)
        conn.execute(
            """INSERT INTO mission (robot_id, state, started_at, updated_at, context) VALUES (?,?,?,?,?)
               ON CONFLICT(robot_id) DO UPDATE SET state=excluded.state, updated_at=excluded.updated_at,
                 context=excluded.context, started_at=excluded.started_at""",
            (robot_id, state, start, now, json.dumps(context or {}, ensure_ascii=False)),
        )


def mission_clear(robot_id: str) -> None:
    with connect() as conn:
        conn.execute("DELETE FROM mission WHERE robot_id=?", (robot_id,))


def device_touch(device_id: str, ip: str | None, rssi: int | None, battery_v: float | None,
                 firmware: str | None, sensors: dict | None, role: str | None = None,
                 capabilities: list | None = None, activity: str | None = None,
                 progress: float | None = None) -> None:
    """Cihaz kalp atışı. İsimli parametreler kullanılır: sıra hatası olmaz."""
    params = {
        "id": device_id,
        "ts": time.time(),
        "ip": ip,
        "rssi": rssi,
        "batt": battery_v,
        "fw": firmware,
        "sensors": json.dumps(sensors or {}, ensure_ascii=False),
        "role": role,
        "caps": json.dumps(capabilities, ensure_ascii=False) if capabilities else None,
        "act": activity,
        "prog": progress,
    }
    with connect() as conn:
        conn.execute(
            """INSERT INTO devices (id, last_seen, ip, rssi, battery_v, firmware, sensors,
                                    sync_count, role, capabilities, activity, progress, activity_at)
               VALUES (:id, :ts, :ip, :rssi, :batt, :fw, :sensors, 1,
                       COALESCE(:role, 'robot'), :caps, :act, :prog,
                       CASE WHEN :act IS NULL THEN NULL ELSE :ts END)
               ON CONFLICT(id) DO UPDATE SET
                 last_seen=:ts, ip=:ip, rssi=:rssi,
                 battery_v=COALESCE(:batt, devices.battery_v),
                 firmware=COALESCE(:fw, devices.firmware),
                 sensors=COALESCE(:sensors, devices.sensors),
                 role=COALESCE(:role, devices.role),
                 capabilities=COALESCE(:caps, devices.capabilities),
                 activity=COALESCE(:act, devices.activity),
                 progress=COALESCE(:prog, devices.progress),
                 activity_at=CASE WHEN :act IS NULL THEN devices.activity_at ELSE :ts END,
                 sync_count=devices.sync_count+1""",
            params,
        )


def device_role(device_id: str) -> str:
    with connect() as conn:
        row = conn.execute("SELECT role FROM devices WHERE id=?", (device_id,)).fetchone()
    return (row["role"] if row and row["role"] else "robot")


def insert_findings(device_id: str, items: list[dict]) -> int:
    now = time.time()
    rows = [(device_id, it.get("scan_id"), now, it["target"], it.get("port"), it.get("proto"),
             it.get("service"), it.get("version"), it.get("severity"), it["title"],
             it.get("evidence"), it.get("cvss"), 1 if it.get("in_scope", True) else 0)
            for it in items]
    if not rows:
        return 0
    with connect() as conn:
        conn.executemany(
            """INSERT INTO findings (device_id, scan_id, ts, target, port, proto, service,
                                     version, severity, title, evidence, cvss, in_scope)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", rows)
    return len(rows)


def findings_recent(device_id: str | None, limit: int = 100, severity: str | None = None) -> list[dict]:
    q = "SELECT * FROM findings"; where, args = [], []
    if device_id:
        where.append("device_id=?"); args.append(device_id)
    if severity:
        where.append("severity=?"); args.append(severity)
    if where:
        q += " WHERE " + " AND ".join(where)
    q += " ORDER BY id DESC LIMIT ?"; args.append(limit)
    with connect() as conn:
        return [dict(r) for r in conn.execute(q, args).fetchall()]


def device_list() -> list[dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute("SELECT * FROM devices ORDER BY id").fetchall()
    out = []
    for r in rows:
        d = dict(r)
        d["sensors"] = json.loads(d["sensors"] or "{}")
        d["capabilities"] = json.loads(d["capabilities"] or "[]")
        d["online"] = bool(d["last_seen"]) and (time.time() - float(d["last_seen"]) < 15)
        out.append(d)
    return out


def flags_get(robot_id: str) -> bool:
    with connect() as conn:
        row = conn.execute("SELECT estopped FROM robot_flags WHERE robot_id=?", (robot_id,)).fetchone()
    return bool(row and row["estopped"])


def flags_set(robot_id: str, estopped: bool) -> None:
    with connect() as conn:
        conn.execute(
            """INSERT INTO robot_flags (robot_id, estopped, updated_at) VALUES (?,?,?)
               ON CONFLICT(robot_id) DO UPDATE SET estopped=excluded.estopped, updated_at=excluded.updated_at""",
            (robot_id, 1 if estopped else 0, time.time()),
        )


def command_enqueue(robot_id: str, kind: str, params: dict | None) -> int:
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO commands (robot_id, ts, kind, params, status) VALUES (?,?,?,?, 'queued')",
            (robot_id, time.time(), kind, json.dumps(params or {}, ensure_ascii=False)),
        )
        return int(cur.lastrowid)


def command_claim_next(robot_id: str, ttl_s: int) -> dict[str, Any] | None:
    now = time.time()
    with connect() as conn:
        conn.execute(
            """UPDATE commands SET status='expired'
               WHERE robot_id=? AND status='claimed' AND claimed_at < ?""",
            (robot_id, now - ttl_s),
        )
        row = conn.execute(
            "SELECT * FROM commands WHERE robot_id=? AND status='queued' ORDER BY id LIMIT 1",
            (robot_id,),
        ).fetchone()
        if not row:
            return None
        conn.execute(
            "UPDATE commands SET status='claimed', claimed_at=? WHERE id=?", (now, row["id"])
        )
    d = dict(row); d["params"] = json.loads(d["params"] or "{}"); d["status"] = "claimed"
    return d


def command_ack(robot_id: str, command_id: int, ok: bool, note: str | None) -> bool:
    with connect() as conn:
        cur = conn.execute(
            """UPDATE commands SET status=?, done_at=?, note=?
               WHERE id=? AND robot_id=? AND status IN ('queued','claimed')""",
            ("done" if ok else "failed", time.time(), note, command_id, robot_id),
        )
        return cur.rowcount > 0


def commands_recent(robot_id: str, limit: int = 50) -> list[dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM commands WHERE robot_id=? ORDER BY id DESC LIMIT ?", (robot_id, limit)
        ).fetchall()
    out = []
    for r in rows:
        d = dict(r); d["params"] = json.loads(d["params"] or "{}"); out.append(d)
    return out


def frames_for_cleanup(camera_id: str, keep: int) -> Iterable[tuple[int, str]]:
    with connect() as conn:
        rows = conn.execute(
            """SELECT id, path FROM frames WHERE camera_id=? AND id NOT IN
               (SELECT id FROM frames WHERE camera_id=? ORDER BY id DESC LIMIT ?)""",
            (camera_id, camera_id, keep),
        ).fetchall()
    return [(int(r["id"]), str(r["path"])) for r in rows]


def delete_frames(pairs: list[tuple[int, str]]) -> None:
    if not pairs:
        return
    with connect() as conn:
        conn.executemany("DELETE FROM frames WHERE id=?", [(i,) for i, _ in pairs])
    for _, p in pairs:
        try:
            Path(p).unlink(missing_ok=True)
        except OSError:
            pass
