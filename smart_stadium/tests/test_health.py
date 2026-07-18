"""Tests for the Health Check API."""


def test_health_check_returns_healthy(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "healthy"
    assert body["data"]["database"] == "up"


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "docs" in body["data"]
