import time
import pytest
from app import main as app_main

BSSID = "aa:bb:cc:dd:ee:ff"
KEY = "tok-1234567890"


@pytest.fixture(autouse=True)
def _cfg(monkeypatch):
    monkeypatch.setattr(app_main, "ATTACK_ENABLE", True)
    monkeypatch.setattr(app_main, "ATTACK_MAX_S", 60)
    monkeypatch.setattr(app_main, "ATTACK_COOLDOWN_S", 0)
    monkeypatch.setattr(app_main, "ATTACK_DAILY_MAX", 10)
    monkeypatch.setenv("ROBO_ATTACK_BSSIDS", BSSID)
    app_main.MIN_INTERVAL_S = 0.0
    yield


def _arm(client, robot):
    r = client.post(f"/api/v1/robots/{robot}/attack/arm")
    assert r.status_code == 200, r.text
    return r.json()["token"]


def _start(client, robot, token, **kw):
    body = {"mode": "deauth", "bssid": BSSID, "channel": 6, "duration_s": 10, "token": token}
    body.update(kw)
    return client.post(f"/api/v1/robots/{robot}/attack", json=body)


def test_attack_disabled_by_default(client, monkeypatch):
    monkeypatch.setattr(app_main, "ATTACK_ENABLE", False)
    assert client.post("/api/v1/robots/a0/attack/arm").status_code == 403


def test_attack_without_targets_rejects_start(client, monkeypatch):
    monkeypatch.setenv("ROBO_ATTACK_BSSIDS", "")
    r = client.post("/api/v1/robots/a1/attack/arm")
    assert r.status_code == 200 and r.json()["allowlist"] == []
    tok = r.json()["token"]
    assert _start(client, "a1", tok).status_code == 403


def test_operator_can_approve_a_target(client, monkeypatch):
    monkeypatch.setenv("ROBO_ATTACK_BSSIDS", "")
    added = client.post("/api/v1/robots/a1b/attack/targets",
                        json={"bssid": BSSID, "note": "test AP", "ttl_hours": 1})
    assert added.status_code == 201, added.text
    arm = client.post("/api/v1/robots/a1b/attack/arm")
    assert BSSID in arm.json()["allowlist"]
    assert _start(client, "a1b", arm.json()["token"]).status_code == 201
    client.post("/api/v1/robots/a1b/attack/stop")
    rm = client.delete(f"/api/v1/robots/a1b/attack/targets/{BSSID}")
    assert rm.status_code == 200 and rm.json()["removed"] is True


def test_attack_requires_valid_token_and_scope(client):
    tok = _arm(client, "a2")
    assert _start(client, "a2", "wrong-token-xx").status_code == 401
    assert _start(client, "a2", tok, bssid="11:22:33:44:55:66").status_code == 403
    assert _start(client, "a2", tok, duration_s=999).status_code == 422
    ok = _start(client, "a2", tok)
    assert ok.status_code == 201, ok.text
    assert ok.json()["status"] == "active"
    kinds = [c["kind"] for c in client.get("/api/v1/robots/a2/commands").json()]
    assert "attack" in kinds


def test_token_is_single_use_and_session_exclusive(client):
    tok = _arm(client, "a3")
    assert _start(client, "a3", tok).status_code == 201
    # aynı token tekrar kullanılamaz
    assert _start(client, "a3", tok).status_code == 401
    # yeni token ile ikinci oturum açılamaz
    tok2 = _arm(client, "a3")
    assert _start(client, "a3", tok2).status_code == 409
    stop = client.post("/api/v1/robots/a3/attack/stop")
    assert stop.status_code == 200 and stop.json()["stopped"] is True


def test_generic_command_endpoint_rejects_attack(client):
    r = client.post("/api/v1/robots/a4/commands", json={"kind": "attack", "params": {}})
    assert r.status_code == 422


def test_daily_budget(client, monkeypatch):
    monkeypatch.setattr(app_main, "ATTACK_DAILY_MAX", 1)
    tok = _arm(client, "a5")
    assert _start(client, "a5", tok).status_code == 201
    client.post("/api/v1/robots/a5/attack/stop")
    tok2 = _arm(client, "a5")
    assert _start(client, "a5", tok2).status_code == 429


def test_watchdog_closes_expired_session(client):
    tok = _arm(client, "a6")
    r = _start(client, "a6", tok, duration_s=5)
    sid = r.json()["session_id"]
    # süreyi geçmişe çek
    from app import db
    with db.connect() as conn:
        conn.execute("UPDATE attack_sessions SET ends_at=? WHERE id=?", (time.time() - 1, sid))
    assert app_main._sweep_attacks() == 1
    st = client.get("/api/v1/robots/a6/attack/status").json()
    assert st["active"] is None
    kinds = [c["kind"] for c in client.get("/api/v1/robots/a6/commands").json()]
    assert kinds.count("stop") >= 1


def test_attack_status_reports_budget(client):
    st = client.get("/api/v1/robots/a7/attack/status").json()
    assert st["enabled"] is True
    assert st["allowlist"] == [BSSID]
    assert st["daily_budget"] == 10
