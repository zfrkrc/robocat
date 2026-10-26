import time
from app import main as app_main


def test_sync_without_keys_is_loopback_only(client):
    r = client.post("/api/v1/device/dev-a/sync", json={"battery_v": 11.7, "rssi": -62})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["robot_id"] == "dev-a"
    assert "config" in body and body["next_poll_s"] >= 1


def test_device_key_required_when_configured(client, monkeypatch):
    monkeypatch.setenv("ROBO_DEVICE_KEYS", "dev-b:s3cret")
    bad = client.post("/api/v1/device/dev-b/sync", json={}, headers={"X-Device-Key": "nope"})
    assert bad.status_code == 401
    missing = client.post("/api/v1/device/dev-b/sync", json={})
    assert missing.status_code == 401
    ok = client.post("/api/v1/device/dev-b/sync", json={}, headers={"X-Device-Key": "s3cret"})
    assert ok.status_code == 200


def test_sync_claims_commands_and_accepts_acks(client):
    app_main.MIN_INTERVAL_S = 0.0
    client.post("/api/v1/robots/dev-c/mission/start")
    r = client.post("/api/v1/device/dev-c/sync", json={})
    assert r.status_code == 200
    cmds = r.json()["commands"]
    assert cmds and cmds[0]["kind"] in ("follow", "say")

    # ack the first command and ensure it leaves the queue
    first = cmds[0]["id"]
    r2 = client.post("/api/v1/device/dev-c/sync", json={"ack": [{"id": first, "ok": True}]})
    assert r2.json()["acks_applied"] == 1
    remaining = [c["kind"] for c in client.get("/api/v1/robots/dev-c/commands").json()
                 if c["status"] in ("queued", "claimed")]
    assert not any(c["id"] == first for c in client.get("/api/v1/robots/dev-c/commands").json()
                   if c["id"] == first and c["status"] in ("queued", "claimed"))


def test_sync_applies_mission_events(client):
    app_main.MIN_INTERVAL_S = 0.0
    client.post("/api/v1/robots/dev-d/mission/start")
    time.sleep(0.01)
    r = client.post("/api/v1/device/dev-d/sync", json={"events": [{"type": "name_called"}]})
    assert r.json()["events_applied"] == 1
    assert client.get("/api/v1/robots/dev-d/mission").json()["state"] == "hold"
    assert [c["kind"] for c in client.get("/api/v1/robots/dev-d/commands").json()].count("stop") >= 1


def test_rate_limit(client, monkeypatch):
    monkeypatch.setattr(app_main, "MIN_INTERVAL_S", 5.0)
    app_main._last_sync.clear()
    assert client.post("/api/v1/device/dev-e/sync", json={}).status_code == 200
    assert client.post("/api/v1/device/dev-e/sync", json={}).status_code == 429
    monkeypatch.setattr(app_main, "MIN_INTERVAL_S", 0.0)


def test_devices_list_reports_online(client):
    app_main.MIN_INTERVAL_S = 0.0
    client.post("/api/v1/device/dev-f/sync", json={"rssi": -55, "firmware": "1.0.0"})
    rows = {d["id"]: d for d in client.get("/api/v1/devices").json()}
    assert rows["dev-f"]["online"] is True
    assert rows["dev-f"]["rssi"] == -55
    assert rows["dev-f"]["firmware"] == "1.0.0"
