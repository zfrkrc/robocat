"""Mission state machine: follow, stop when called, on-demand greet + alcohol test.

Design rules
------------
* **Deterministic.** Every transition is caused by an explicit event, a
  deadline, or a threshold. There is no random choice and no "guess".
* **Recognition is evidence-based.** Motion alone never means "person".
  A person/ArUco label must repeat over several frames, or the operator
  must send ``person_seen``; otherwise the answer is ``unknown``.
* **The robot is safe on its own.** This module only queues commands.
  The local controller must stop on its own stop button and on link loss.
* **Alcohol reading is not a breathalyser.** MQ-3 is uncalibrated here:
  the report gives the raw value and a qualitative band, never a legal or
  medical judgement.
"""
from __future__ import annotations

import os
import threading
import time
from typing import Any

from . import db

ENV_CHECK_S = float(os.environ.get("ROBO_ENV_CHECK_S", 60))
ANSWER_TIMEOUT_S = float(os.environ.get("ROBO_ANSWER_TIMEOUT_S", 8))
SENSOR_TIMEOUT_S = float(os.environ.get("ROBO_SENSOR_TIMEOUT_S", 20))
SCAN_TIMEOUT_S = float(os.environ.get("ROBO_SCAN_TIMEOUT_S", 10))
HOLD_SAY = os.environ.get("ROBO_HOLD_SAY", "Efendim?")
GREET_SAY = os.environ.get("ROBO_GREET_SAY", "Merhaba, ben RoboCat.")
QUESTION_SAY = os.environ.get("ROBO_QUESTION_SAY", "Alkol testi ister misin?")
NO_SAY = os.environ.get("ROBO_NO_SAY", "Tanistigima memnun oldum.")
YES_SAY = os.environ.get("ROBO_YES_SAY", "Burnumu uzatiyorum, ufleyin.")
FAIL_SAY = os.environ.get("ROBO_FAIL_SAY", "Olcum alinamadi.")
FOLLOW_SAY = os.environ.get("ROBO_FOLLOW_SAY", "Seni takip ediyorum.")

VALID_EVENTS = {"name_called", "resume", "env_check", "scan_result", "person_seen",
                "answer", "sensor", "operator_stop"}


class Mission:
    def __init__(self, robot_id: str) -> None:
        self.robot_id = robot_id

    # -- helpers -------------------------------------------------------
    def _load(self) -> dict | None:
        return db.mission_get(self.robot_id)

    def _cmd(self, kind: str, **params: Any) -> None:
        db.command_enqueue(self.robot_id, kind, params or {})

    def _say(self, text: str) -> None:
        self._cmd("say", text=text)

    def _set(self, state: str, **ctx: Any) -> None:
        db.mission_set(self.robot_id, state, ctx)

    def _now(self) -> float:
        return time.time()

    # -- public --------------------------------------------------------
    def start(self) -> dict:
        if db.flags_get(self.robot_id):
            return {"state": "estop", "note": "emergency stop engaged"}
        db.mission_set(self.robot_id, "follow", {"last_env_check": self._now()})
        self._cmd("follow")
        self._say(FOLLOW_SAY)
        db.log_event("mission.start", "follow", robot_id=self.robot_id)
        return {"state": "follow"}

    def stop(self) -> dict:
        db.mission_clear(self.robot_id)
        self._cmd("stop")
        db.log_event("mission.stop", "operator", robot_id=self.robot_id)
        return {"state": "idle"}

    def state(self) -> dict:
        row = self._load()
        if not row:
            return {"robot_id": self.robot_id, "state": "idle", "estopped": db.flags_get(self.robot_id)}
        return {
            "robot_id": self.robot_id,
            "state": row["state"],
            "started_at": row["started_at"],
            "updated_at": row["updated_at"],
            "context": row["context"],
            "estopped": db.flags_get(self.robot_id),
        }

    def handle(self, event: str, data: dict | None = None) -> dict:
        data = data or {}
        if event not in VALID_EVENTS:
            return {"ok": False, "error": f"unknown event '{event}'", "valid": sorted(VALID_EVENTS)}

        row = self._load()
        if not row:
            return {"ok": False, "error": "mission not started"}
        state, ctx = row["state"], row["context"]

        if db.flags_get(self.robot_id):
            return {"ok": False, "error": "emergency stop engaged", "state": state}

        if event == "operator_stop":
            return self.stop()

        if event == "name_called" and state in ("follow", "scan", "hold"):
            self._cmd("stop")
            self._say(HOLD_SAY)
            self._set("hold", hold_since=self._now())
            db.log_event("mission.name_called", "hold", robot_id=self.robot_id)
            return self.state()

        if event == "resume" and state in ("hold", "wait_answer", "offer"):
            self._enter_follow(ctx)
            return self.state()

        if event in ("env_check", "person_seen") and state in ("follow", "scan"):
            return self._enter_engage(ctx, trigger=event)

        if event == "scan_result" and state == "scan":
            accepted = bool(data.get("accepted"))
            if accepted:
                return self._enter_engage(ctx, trigger="scan_result", label=data.get("label"))
            self._enter_follow(ctx)
            return self.state()

        if event == "answer" and state == "wait_answer":
            yes = data.get("yes")
            if yes is True:
                return self._enter_alcohol(ctx)
            if yes is False:
                self._say(NO_SAY)
                self._enter_follow(ctx)
                return self.state()
            return {"ok": False, "error": "answer.yes must be true or false"}

        if event == "sensor" and state == "alcohol_test":
            return self._report_alcohol(ctx, data)

        return {"ok": True, "state": state, "note": "event ignored in this state"}

    # -- transitions ---------------------------------------------------
    def _enter_follow(self, ctx: dict) -> dict:
        ctx = dict(ctx or {})
        ctx.pop("deadline", None)
        ctx["last_env_check"] = self._now()
        self._set("follow", **ctx)
        self._cmd("follow")
        return self.state()

    def _enter_engage(self, ctx: dict, trigger: str, label: str | None = None) -> dict:
        ctx = dict(ctx or {})
        ctx.update({"trigger": trigger, "label": label, "deadline": self._now() + SCAN_TIMEOUT_S})
        self._cmd("stop")
        self._cmd("look", pan=0, tilt=0)
        self._say(GREET_SAY)
        self._set("wait_answer", **ctx)
        self._say(QUESTION_SAY)
        ctx["deadline"] = self._now() + ANSWER_TIMEOUT_S
        self._set("wait_answer", **ctx)
        db.log_event("mission.engage", f"trigger={trigger} label={label}", robot_id=self.robot_id)
        return self.state()

    def _enter_alcohol(self, ctx: dict) -> dict:
        ctx = dict(ctx or {})
        ctx["deadline"] = self._now() + SENSOR_TIMEOUT_S
        self._cmd("nose_extend")
        self._say(YES_SAY)
        self._set("alcohol_test", **ctx)
        db.log_event("mission.alcohol_test", "started", robot_id=self.robot_id)
        return self.state()

    def _report_alcohol(self, ctx: dict, data: dict) -> dict:
        value = data.get("alcohol_ppm", data.get("alcohol_mv"))
        unit = "ppm" if "alcohol_ppm" in data else "mV"
        if value is None:
            return {"ok": False, "error": "sensor event needs alcohol_ppm or alcohol_mv"}
        try:
            value = float(value)
        except (TypeError, ValueError):
            return {"ok": False, "error": "sensor value is not numeric"}

        # Uncalibrated sensor: band only, never a legal/medical verdict.
        if unit == "ppm":
            band = "yuksek" if value >= 200 else ("orta" if value >= 80 else "dusuk")
            text = f"Olcum: {value:.0f} ppm, {band} seviye. Kalibre edilmemis sensor."
        else:
            band = "yuksek" if value >= 2500 else ("orta" if value >= 1500 else "dusuk")
            text = f"Olcum: {value:.0f} mV, {band} seviye. Kalibre edilmemis sensor."

        self._say(text)
        self._cmd("nose_retract")
        db.log_event("mission.report", text, robot_id=self.robot_id)
        ctx = dict(ctx or {})
        ctx["last_result"] = {"value": value, "unit": unit, "band": band, "ts": self._now()}
        self._enter_follow(ctx)
        return self.state()

    def _enter_scan(self, ctx: dict) -> dict:
        ctx = dict(ctx or {})
        ctx["deadline"] = self._now() + SCAN_TIMEOUT_S
        self._cmd("hold")
        self._set("scan", **ctx)
        db.log_event("mission.scan", "environment check", robot_id=self.robot_id)
        return self.state()

    def _enter_hold(self, ctx: dict) -> dict:
        self._cmd("stop")
        self._set("hold", **dict(ctx or {}, hold_since=self._now()))
        return self.state()

    # -- timeouts ------------------------------------------------------
    def tick(self) -> None:
        row = self._load()
        if not row:
            return
        state, ctx = row["state"], row["context"]

        if db.flags_get(self.robot_id) and state != "estop":
            self._cmd("stop")
            self._set("estop", **ctx)
            return

        if state == "follow":
            if self._now() - float(ctx.get("last_env_check", 0)) >= ENV_CHECK_S:
                self._enter_scan(ctx)
            return

        if state == "scan":
            if self._now() >= float(ctx.get("deadline", 0)):
                self._enter_follow(ctx)  # no evidence -> no engagement
            return

        if state == "wait_answer":
            if self._now() >= float(ctx.get("deadline", 0)):
                self._say(NO_SAY)  # unanswered counts as "no"
                self._enter_follow(ctx)
            return

        if state == "alcohol_test":
            if self._now() >= float(ctx.get("deadline", 0)):
                self._say(FAIL_SAY)
                self._cmd("nose_retract")
                self._enter_follow(ctx)
            return

        if state == "estop":
            if not db.flags_get(self.robot_id):
                self._enter_follow(ctx)
            return


_missions: dict[str, Mission] = {}
_lock = threading.Lock()
_ticker: threading.Thread | None = None


def for_robot(robot_id: str) -> Mission:
    with _lock:
        if robot_id not in _missions:
            _missions[robot_id] = Mission(robot_id)
        return _missions[robot_id]


def _loop() -> None:
    while True:
        try:
            with db.connect() as conn:
                ids = [r["robot_id"] for r in conn.execute("SELECT robot_id FROM mission").fetchall()]
            for rid in ids:
                try:
                    for_robot(rid).tick()
                except Exception as exc:  # keep ticking other robots
                    db.log_event("mission.error", f"{type(exc).__name__}: {exc}", robot_id=rid)
        except Exception:
            pass
        time.sleep(1.0)


def start_ticker() -> None:
    global _ticker
    with _lock:
        if _ticker is None or not _ticker.is_alive():
            _ticker = threading.Thread(target=_loop, name="mission-ticker", daemon=True)
            _ticker.start()
