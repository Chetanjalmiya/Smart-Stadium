"""Tests for the Food & Beverage module."""


def _create_menu_item(client, **overrides):
    payload = {"name": "Stadium Burger", "category": "Main Course", "price": 8.5, "stall_location": "Stall 1"}
    payload.update(overrides)
    return client.post("/api/v1/food/menu", json=payload)


def test_create_menu_item(client):
    response = _create_menu_item(client)
    assert response.status_code == 201
    assert response.json()["data"]["price"] == 8.5


def test_place_order_calculates_total(client):
    item = _create_menu_item(client).json()["data"]
    response = client.post(
        "/api/v1/food/orders",
        json={"customer_name": "Alice", "seat_number": "A1-1", "items": [{"menu_item_id": item["id"], "quantity": 3}]},
    )
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["total_amount"] == 25.5
    assert body["status"] == "placed"


def test_place_order_unavailable_item_fails(client):
    item = _create_menu_item(client, is_available=False).json()["data"]
    response = client.post(
        "/api/v1/food/orders",
        json={"customer_name": "Alice", "items": [{"menu_item_id": item["id"], "quantity": 1}]},
    )
    assert response.status_code == 422


def test_place_order_invalid_menu_item_fails(client):
    response = client.post(
        "/api/v1/food/orders",
        json={"customer_name": "Alice", "items": [{"menu_item_id": 9999, "quantity": 1}]},
    )
    assert response.status_code == 404


def test_update_order_status(client):
    item = _create_menu_item(client).json()["data"]
    order = client.post(
        "/api/v1/food/orders",
        json={"customer_name": "Alice", "items": [{"menu_item_id": item["id"], "quantity": 1}]},
    ).json()["data"]
    response = client.patch(f"/api/v1/food/orders/{order['id']}/status", json={"status": "ready"})
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "ready"
