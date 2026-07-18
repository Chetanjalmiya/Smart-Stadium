"""Tests for the Notifications module."""


def _create_notification(client, **overrides):
    payload = {"title": "Match Starting Soon", "message": "The match will begin in 15 minutes.", "category": "match"}
    payload.update(overrides)
    return client.post("/api/v1/notifications", json=payload)


def test_create_notification(client):
    response = _create_notification(client)
    assert response.status_code == 201
    assert response.json()["data"]["is_read"] is False


def test_mark_notification_as_read(client):
    notification = _create_notification(client).json()["data"]
    response = client.post(f"/api/v1/notifications/{notification['id']}/read")
    assert response.status_code == 200
    assert response.json()["data"]["is_read"] is True


def test_list_unread_notifications(client):
    n1 = _create_notification(client).json()["data"]
    _create_notification(client, title="Another update")
    client.post(f"/api/v1/notifications/{n1['id']}/read")
    response = client.get("/api/v1/notifications", params={"unread_only": True})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
