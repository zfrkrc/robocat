def test_health(client):
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["detector"]["detector"] in ("motion", "yolo", "none")


def test_register_and_list(client):
    r = client.post("/api/v1/cameras", json={"id": "head-left", "name": "Sol kafa", "role": "head_left"})
    assert r.status_code == 201, r.text
    r = client.get("/api/v1/cameras")
    ids = [c["id"] for c in r.json()]
    assert "head-left" in ids


def test_frame_ingest_sync_and_latest(client, jpeg_factory):
    client.post("/api/v1/cameras", json={"id": "cam-a", "name": "A", "role": "head_right"})
    f1 = jpeg_factory()
    r = client.post("/api/v1/cameras/cam-a/frame?sync=1", content=f1,
                    headers={"Content-Type": "image/jpeg"})
    assert r.status_code == 202, r.text
    body = r.json()
    assert body["analysis"]["width"] == 320 and body["analysis"]["height"] == 240
    assert body["analysis"]["detector"] == "motion"
    got = client.get("/api/v1/cameras/cam-a/latest.jpg")
    assert got.status_code == 200 and got.content[:2] == b"\xff\xd8"


def test_motion_detection_between_frames(client, jpeg_factory):
    client.post("/api/v1/cameras", json={"id": "cam-b", "name": "B", "role": "arm"})
    client.post("/api/v1/cameras/cam-b/frame?sync=1", content=jpeg_factory(),
                headers={"Content-Type": "image/jpeg"})
    r = client.post("/api/v1/cameras/cam-b/frame?sync=1", content=jpeg_factory((120, 90, 240, 200)),
                    headers={"Content-Type": "image/jpeg"})
    assert r.status_code == 202
    dets = client.get("/api/v1/cameras/cam-b/detections").json()
    assert any(d["kind"] == "motion" for d in dets), dets


def test_rejects_non_jpeg(client):
    client.post("/api/v1/cameras", json={"id": "cam-c", "name": "C", "role": "other"})
    r = client.post("/api/v1/cameras/cam-c/frame", content=b"not-an-image",
                    headers={"Content-Type": "image/jpeg"})
    assert r.status_code == 415


def test_unknown_camera(client, jpeg_factory):
    r = client.post("/api/v1/cameras/nope/frame", content=jpeg_factory(),
                    headers={"Content-Type": "image/jpeg"})
    assert r.status_code == 404


def test_telemetry_and_state(client):
    r = client.post("/api/v1/robots/robocat-1/telemetry",
                    json={"battery_v": 11.8, "current_a": 2.4, "imu": {"pitch": 1.2}})
    assert r.status_code == 201, r.text
    s = client.get("/api/v1/robots/robocat-1/state").json()
    assert s["telemetry"]["battery_v"] == 11.8
    assert s["estopped"] is False


def test_command_queue_claim_ack(client):
    r = client.post("/api/v1/robots/robocat-1/commands", json={"kind": "move", "params": {"linear": 0.1}})
    assert r.status_code == 201
    cmd = r.json()
    nxt = client.get("/api/v1/robots/robocat-1/commands/next").json()
    assert nxt and nxt["id"] == cmd["id"] and nxt["status"] == "claimed"
    ack = client.post(f"/api/v1/robots/robocat-1/commands/{cmd['id']}/ack", json={"ok": True})
    assert ack.status_code == 200
    again = client.post(f"/api/v1/robots/robocat-1/commands/{cmd['id']}/ack", json={"ok": True})
    assert again.status_code == 404


def test_emergency_stop_blocks_non_stop(client):
    client.post("/api/v1/robots/robocat-2/emergency_stop", json={"engaged": True})
    blocked = client.post("/api/v1/robots/robocat-2/commands", json={"kind": "move", "params": {}})
    assert blocked.status_code == 409
    allowed = client.post("/api/v1/robots/robocat-2/commands", json={"kind": "stop", "params": {}})
    assert allowed.status_code == 201
    client.post("/api/v1/robots/robocat-2/emergency_stop", json={"engaged": False})
    ok = client.post("/api/v1/robots/robocat-2/commands", json={"kind": "move", "params": {}})
    assert ok.status_code == 201
