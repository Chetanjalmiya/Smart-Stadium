"""Tests for the Analytics module."""
from datetime import datetime, timedelta


def test_dashboard_summary_structure(client):
    response = client.get("/api/v1/analytics/dashboard")
    assert response.status_code == 200
    data = response.json()["data"]
    for key in ["tickets", "matches", "parking", "food", "crowd", "safety", "feedback"]:
        assert key in data


def test_ticket_analytics_reflects_data(client):
    match = client.post(
        "/api/v1/matches",
        json={
            "home_team": "A",
            "away_team": "B",
            "scheduled_time": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        },
    ).json()["data"]
    client.post(
        "/api/v1/tickets",
        json={
            "match_id": match["id"],
            "holder_name": "John",
            "holder_email": "john@example.com",
            "price": 20.0,
        },
    )
    response = client.get("/api/v1/analytics/tickets")
    assert response.status_code == 200
    assert response.json()["data"]["total_tickets_issued"] == 1
    assert response.json()["data"]["total_revenue"] == 20.0
