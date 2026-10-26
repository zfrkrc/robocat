import time


def _cmds(client, robot):
    return client.get(f"/api/v1/robots/{robot}/commands").json()


def _kinds(client, robot):
    return [c["kind"] for c in _cmds(client, robot)]


def test_mission_start_queues_follow(client):
    r = client.post("/api/v1/robots/m1/mission/start")
    assert r.status_code == 200 and r.json()["state"] == "follow"
    assert "follow" in _kinds(client, "m1")


def test_name_called_stops(client):
    client.post("/api/v1/robots/m2/mission/start")
    r = client.post("/api/v1/robots/m2/mission/event", json={"type": "name_called"})
    assert r.json()["state"] == "hold"
    k = _kinds(client, "m2")
    assert "stop" in k
    says = [c for c in _cmds(client, "m2") if c["kind"] == "say"]
    assert says and "Efendim" in says[0]["params"]["text"]


def test_env_check_then_yes_runs_alcohol_test(client):
    client.post("/api/v1/robots/m3/mission/start")
    r = client.post("/api/v1/robots/m3/mission/event", json={"type": "env_check"})
    assert r.json()["state"] == "wait_answer"
    r = client.post("/api/v1/robots/m3/mission/event", json={"type": "answer", "data": {"yes": True}})
    assert r.json()["state"] == "alcohol_test"
    k = _kinds(client, "m3")
    assert "nose_extend" in k
    r = client.post("/api/v1/robots/m3/mission/event",
                    json={"type": "sensor", "data": {"alcohol_ppm": 90}})
    body = r.json()
    assert body["state"] == "follow"
    assert body["context"]["last_result"]["value"] == 90
    assert "nose_retract" in _kinds(client, "m3")
    texts = [c["params"]["text"] for c in _cmds(client, "m3") if c["kind"] == "say"]
    assert any("ppm" in t for t in texts)


def test_answer_no_returns_to_follow(client):
    client.post("/api/v1/robots/m4/mission/start")
    client.post("/api/v1/robots/m4/mission/event", json={"type": "env_check"})
    r = client.post("/api/v1/robots/m4/mission/event", json={"type": "answer", "data": {"yes": False}})
    assert r.json()["state"] == "follow"


def test_unanswered_question_times_out_to_follow(client):
    client.post("/api/v1/robots/m5/mission/start")
    client.post("/api/v1/robots/m5/mission/event", json={"type": "env_check"})
    time.sleep(1.4)
    from app import mission
    mission.for_robot("m5").tick()
    assert client.get("/api/v1/robots/m5/mission").json()["state"] == "follow"


def test_sensor_timeout_retracts_nose(client):
    client.post("/api/v1/robots/m6/mission/start")
    client.post("/api/v1/robots/m6/mission/event", json={"type": "env_check"})
    client.post("/api/v1/robots/m6/mission/event", json={"type": "answer", "data": {"yes": True}})
    time.sleep(1.4)
    from app import mission
    mission.for_robot("m6").tick()
    assert client.get("/api/v1/robots/m6/mission").json()["state"] == "follow"
    assert "nose_retract" in _kinds(client, "m6")


def test_estop_blocks_mission_and_stops_it(client):
    client.post("/api/v1/robots/m7/mission/start")
    client.post("/api/v1/robots/m7/emergency_stop", json={"engaged": True})
    from app import mission
    mission.for_robot("m7").tick()
    assert client.get("/api/v1/robots/m7/mission").json()["state"] == "estop"
    r = client.post("/api/v1/robots/m7/mission/event", json={"type": "name_called"})
    assert r.status_code == 409
    client.post("/api/v1/robots/m7/emergency_stop", json={"engaged": False})
    mission.for_robot("m7").tick()
    assert client.get("/api/v1/robots/m7/mission").json()["state"] == "follow"


def test_recognition_motion_is_not_accepted(client, jpeg_factory):
    make = jpeg_factory
    client.post("/api/v1/cameras", json={"id": "rc1", "name": "R", "role": "head_left"})
    for marker in (None, (100, 80, 220, 200)):
        client.post("/api/v1/cameras/rc1/frame?sync=1", content=make(marker),
                    headers={"Content-Type": "image/jpeg"})
    r = client.get("/api/v1/robots/r1/recognize?camera_id=rc1").json()
    assert r["accepted"] is False
    assert r["reason"] == "insufficient_evidence"


def test_recognition_requires_repeated_aruco(client, aruco_factory):
    make_aruco = aruco_factory
    client.post("/api/v1/cameras", json={"id": "rc2", "name": "R2", "role": "head_right"})
    for _ in range(2):
        client.post("/api/v1/cameras/rc2/frame?sync=1", content=make_aruco(7),
                    headers={"Content-Type": "image/jpeg"})
    r = client.get("/api/v1/robots/r2/recognize?camera_id=rc2").json()
    assert r["accepted"] is True and r["label"] == "marker_7" and r["hits"] >= 2


def test_single_frame_is_not_enough(client, aruco_factory):
    make_aruco = aruco_factory
    client.post("/api/v1/cameras", json={"id": "rc3", "name": "R3", "role": "arm"})
    client.post("/api/v1/cameras/rc3/frame?sync=1", content=make_aruco(9),
                headers={"Content-Type": "image/jpeg"})
    r = client.get("/api/v1/robots/r3/recognize?camera_id=rc3&min_hits=2").json()
    assert r["accepted"] is False
