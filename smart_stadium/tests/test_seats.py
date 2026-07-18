"""Tests for the Seat Finder module."""


def _create_seat(client, **overrides):
    payload = {
        "seat_number": "B2-3",
        "section": "Section B",
        "row": "2",
        "gate": "Gate B",
        "is_accessible": False,
        "category": "general",
    }
    payload.update(overrides)
    return client.post("/api/v1/seats", json=payload)


def test_create_seat_success(client):
    response = _create_seat(client)
    assert response.status_code == 201
    assert response.json()["data"]["seat_number"] == "B2-3"


def test_create_duplicate_seat_fails(client):
    _create_seat(client)
    response = _create_seat(client)
    assert response.status_code == 409


def test_find_seat_by_number(client):
    _create_seat(client)
    response = client.get("/api/v1/seats/B2-3")
    assert response.status_code == 200
    assert response.json()["data"]["section"] == "Section B"


def test_find_seat_not_found(client):
    response = client.get("/api/v1/seats/ZZZ-9")
    assert response.status_code == 404


def test_list_seats_available_only(client):
    _create_seat(client)
    _create_seat(client, seat_number="B2-4")
    client.patch("/api/v1/seats/B2-4/occupancy", params={"occupied": True})
    response = client.get("/api/v1/seats", params={"available_only": True})
    assert response.status_code == 200
    numbers = [s["seat_number"] for s in response.json()["data"]]
    assert "B2-4" not in numbers
    assert "B2-3" in numbers
