"""Tests for the Live Match Information & Match Schedule module."""
from datetime import datetime, timedelta


def _create_match(client, **overrides):
    payload = {
        "home_team": "Falcons FC",
        "away_team": "Eagles United",
        "venue": "Main Arena",
        "scheduled_time": (datetime.utcnow() + timedelta(days=1)).isoformat(),
    }
    payload.update(overrides)
    return client.post("/api/v1/matches", json=payload)


def test_create_match_success(client):
    response = _create_match(client)
    assert response.status_code == 201
    body = response.json()
    assert body["data"]["home_team"] == "Falcons FC"
    assert body["data"]["status"] == "scheduled"


def test_create_match_missing_field_fails_validation(client):
    response = client.post("/api/v1/matches", json={"home_team": "Falcons FC"})
    assert response.status_code == 422


def test_list_matches(client):
    _create_match(client)
    _create_match(client, home_team="Titans SC", away_team="Warriors FC")
    response = client.get("/api/v1/matches")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2


def test_get_match_not_found(client):
    response = client.get("/api/v1/matches/999")
    assert response.status_code == 404
    assert response.json()["success"] is False


def test_update_match_live_score(client):
    created = _create_match(client).json()["data"]
    response = client.patch(
        f"/api/v1/matches/{created['id']}",
        json={"status": "live", "home_score": 2, "away_score": 1, "current_minute": 60},
    )
    assert response.status_code == 200
    body = response.json()["data"]
    assert body["status"] == "live"
    assert body["home_score"] == 2


def test_delete_match(client):
    created = _create_match(client).json()["data"]
    response = client.delete(f"/api/v1/matches/{created['id']}")
    assert response.status_code == 200
    follow_up = client.get(f"/api/v1/matches/{created['id']}")
    assert follow_up.status_code == 404


def test_get_live_matches(client):
    created = _create_match(client).json()["data"]
    client.patch(f"/api/v1/matches/{created['id']}", json={"status": "live"})
    response = client.get("/api/v1/matches/live")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


def test_get_schedule(client):
    _create_match(client)
    response = client.get("/api/v1/matches/schedule")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
