"""Tests for the Crowd Density Monitoring module."""


def _record(client, **overrides):
    payload = {"zone": "North Stand", "current_count": 450, "capacity": 500}
    payload.update(overrides)
    return client.post("/api/v1/crowd", json=payload)


def test_record_density_calculates_percentage_and_risk(client):
    response = _record(client)
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["density_percentage"] == 90.0
    assert body["risk_level"] == "critical"


def test_record_density_moderate_risk(client):
    response = _record(client, current_count=250, capacity=500)
    body = response.json()["data"]
    assert body["density_percentage"] == 50.0
    assert body["risk_level"] == "moderate"


def test_get_latest_by_zone_not_found(client):
    response = client.get("/api/v1/crowd/Nonexistent")
    assert response.status_code == 404


def test_get_all_latest_zones(client):
    _record(client, zone="North Stand")
    _record(client, zone="South Stand", current_count=100, capacity=500)
    response = client.get("/api/v1/crowd/latest")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2


def test_get_history_for_zone(client):
    _record(client)
    _record(client, current_count=460)
    response = client.get("/api/v1/crowd/North Stand/history")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2
