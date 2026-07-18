"""Tests for the Smart Parking module."""


def _create_slot(client, **overrides):
    payload = {"slot_number": "P1-01", "zone": "P1", "vehicle_type": "car", "hourly_rate": 5.0}
    payload.update(overrides)
    return client.post("/api/v1/parking/slots", json=payload)


def test_create_parking_slot(client):
    response = _create_slot(client)
    assert response.status_code == 201
    assert response.json()["data"]["status"] == "available"


def test_create_duplicate_slot_fails(client):
    _create_slot(client)
    response = _create_slot(client)
    assert response.status_code == 409


def test_book_parking_slot(client):
    slot = _create_slot(client).json()["data"]
    response = client.post(
        "/api/v1/parking/bookings",
        json={"slot_id": slot["id"], "vehicle_number": "XYZ-123", "visitor_name": "Jane Doe"},
    )
    assert response.status_code == 201
    slot_check = client.get(f"/api/v1/parking/slots", params={"zone": "P1"}).json()["data"][0]
    assert slot_check["status"] == "occupied"


def test_book_unavailable_slot_fails(client):
    slot = _create_slot(client).json()["data"]
    client.post(
        "/api/v1/parking/bookings",
        json={"slot_id": slot["id"], "vehicle_number": "XYZ-123", "visitor_name": "Jane Doe"},
    )
    response = client.post(
        "/api/v1/parking/bookings",
        json={"slot_id": slot["id"], "vehicle_number": "ABC-999", "visitor_name": "Bob Smith"},
    )
    assert response.status_code == 409


def test_release_booking_frees_slot(client):
    slot = _create_slot(client).json()["data"]
    booking = client.post(
        "/api/v1/parking/bookings",
        json={"slot_id": slot["id"], "vehicle_number": "XYZ-123", "visitor_name": "Jane Doe"},
    ).json()["data"]
    response = client.post(f"/api/v1/parking/bookings/{booking['id']}/release")
    assert response.status_code == 200
    slot_check = client.get(f"/api/v1/parking/slots", params={"zone": "P1"}).json()["data"][0]
    assert slot_check["status"] == "available"


def test_parking_availability_summary(client):
    _create_slot(client)
    _create_slot(client, slot_number="P1-02")
    response = client.get("/api/v1/parking/availability")
    assert response.status_code == 200
    assert response.json()["data"]["total_slots"] == 2
