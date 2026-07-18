"""Tests for the Stadium Information module."""


def test_create_and_get_stadium_info(client):
    response = client.post(
        "/api/v1/stadium-info",
        json={"key": "hours", "title": "Operating Hours", "content": "Open 3 hours before kickoff."},
    )
    assert response.status_code == 201
    fetched = client.get("/api/v1/stadium-info/hours")
    assert fetched.status_code == 200
    assert fetched.json()["data"]["title"] == "Operating Hours"


def test_duplicate_info_key_fails(client):
    payload = {"key": "rules", "title": "Rules", "content": "No smoking."}
    client.post("/api/v1/stadium-info", json=payload)
    response = client.post("/api/v1/stadium-info", json=payload)
    assert response.status_code == 409


def test_update_stadium_info(client):
    client.post("/api/v1/stadium-info", json={"key": "contact", "title": "Contact", "content": "Call us."})
    response = client.put("/api/v1/stadium-info/contact", json={"content": "Call +1-800-555-0199."})
    assert response.status_code == 200
    assert "555" in response.json()["data"]["content"]


def test_create_and_list_amenities(client):
    client.post(
        "/api/v1/stadium-info/amenities",
        json={"name": "ATM", "category": "services", "location": "Near Gate B"},
    )
    response = client.get("/api/v1/stadium-info/amenities")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
