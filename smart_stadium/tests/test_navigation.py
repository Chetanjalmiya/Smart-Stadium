"""Tests for the Stadium Navigation module."""


def _create_point(client, **overrides):
    payload = {
        "name": "Main Entrance",
        "category": "entrance",
        "zone": "North",
        "pos_x": 0,
        "pos_y": 0,
    }
    payload.update(overrides)
    return client.post("/api/v1/navigation/points", json=payload)


def test_create_navigation_point(client):
    response = _create_point(client)
    assert response.status_code == 201
    assert response.json()["data"]["name"] == "Main Entrance"


def test_list_navigation_points_by_zone(client):
    _create_point(client)
    _create_point(client, name="Gate B", zone="East", pos_x=50, pos_y=20)
    response = client.get("/api/v1/navigation/points", params={"zone": "East"})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


def test_get_route_between_points(client):
    origin = _create_point(client).json()["data"]
    dest = _create_point(client, name="Food Court", zone="Central", pos_x=30, pos_y=40).json()["data"]
    response = client.get(
        "/api/v1/navigation/route",
        params={"origin_id": origin["id"], "destination_id": dest["id"]},
    )
    assert response.status_code == 200
    body = response.json()["data"]
    assert body["distance_units"] > 0
    assert body["estimated_walk_minutes"] > 0


def test_get_route_invalid_point_fails(client):
    origin = _create_point(client).json()["data"]
    response = client.get(
        "/api/v1/navigation/route",
        params={"origin_id": origin["id"], "destination_id": 9999},
    )
    assert response.status_code == 404
