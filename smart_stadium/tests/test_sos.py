"""Tests for the Emergency SOS module."""


def _create_sos(client, **overrides):
    payload = {
        "requester_name": "John Doe",
        "contact_number": "+1234567890",
        "sos_type": "medical",
        "location": "Section A, Row 3",
    }
    payload.update(overrides)
    return client.post("/api/v1/sos", json=payload)


def test_create_sos_request(client):
    response = _create_sos(client)
    assert response.status_code == 201
    assert response.json()["data"]["status"] == "open"


def test_update_sos_status_to_resolved_sets_timestamp(client):
    sos = _create_sos(client).json()["data"]
    response = client.patch(f"/api/v1/sos/{sos['id']}/status", json={"status": "resolved"})
    assert response.status_code == 200
    body = response.json()["data"]
    assert body["status"] == "resolved"
    assert body["resolved_at"] is not None


def test_list_sos_filtered_by_status(client):
    _create_sos(client)
    _create_sos(client, requester_name="Jane Doe")
    response = client.get("/api/v1/sos", params={"status": "open"})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2
