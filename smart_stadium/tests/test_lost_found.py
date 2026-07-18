"""Tests for the Lost & Found module."""


def _create_item(client, **overrides):
    payload = {
        "item_type": "lost",
        "item_name": "Blue Backpack",
        "location": "Gate A",
        "reporter_name": "John Doe",
        "contact_number": "+1234567890",
    }
    payload.update(overrides)
    return client.post("/api/v1/lost-found", json=payload)


def test_create_lost_item(client):
    response = _create_item(client)
    assert response.status_code == 201
    assert response.json()["data"]["status"] == "reported"


def test_search_items_by_keyword(client):
    _create_item(client)
    _create_item(client, item_name="Red Wallet", item_type="found")
    response = client.get("/api/v1/lost-found/search", params={"keyword": "backpack"})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


def test_update_item_status_to_claimed(client):
    item = _create_item(client).json()["data"]
    response = client.patch(f"/api/v1/lost-found/{item['id']}/status", json={"status": "claimed"})
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "claimed"
