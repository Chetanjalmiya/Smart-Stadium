"""Tests for the Admin APIs module."""


def test_admin_overview_requires_key(client):
    response = client.get("/api/v1/admin/overview")
    assert response.status_code == 401


def test_admin_overview_with_valid_key(client, admin_headers):
    response = client.get("/api/v1/admin/overview", headers=admin_headers)
    assert response.status_code == 200
    assert "total_matches" in response.json()["data"]


def test_admin_overview_invalid_key_rejected(client):
    response = client.get("/api/v1/admin/overview", headers={"X-Admin-Key": "wrong-key"})
    assert response.status_code == 401


def test_admin_dashboard_with_valid_key(client, admin_headers):
    response = client.get("/api/v1/admin/dashboard", headers=admin_headers)
    assert response.status_code == 200


def test_admin_reset_database(client, admin_headers):
    client.post("/api/v1/feedback", json={"visitor_name": "A", "rating": 5})
    response = client.delete("/api/v1/admin/reset-database", headers=admin_headers)
    assert response.status_code == 200
    remaining = client.get("/api/v1/feedback").json()["data"]
    assert len(remaining) == 0
