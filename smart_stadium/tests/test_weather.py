"""Tests for the Weather Alerts module."""


def _create_alert(client, **overrides):
    payload = {"title": "Heavy Rain Warning", "description": "Expect heavy rainfall this evening.", "severity": "high"}
    payload.update(overrides)
    return client.post("/api/v1/weather", json=payload)


def test_create_weather_alert(client):
    response = _create_alert(client)
    assert response.status_code == 201
    assert response.json()["data"]["severity"] == "high"


def test_list_active_alerts_only(client):
    alert = _create_alert(client).json()["data"]
    client.post(f"/api/v1/weather/{alert['id']}/deactivate")
    response = client.get("/api/v1/weather", params={"active_only": True})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 0


def test_get_alert_not_found(client):
    response = client.get("/api/v1/weather/999")
    assert response.status_code == 404
