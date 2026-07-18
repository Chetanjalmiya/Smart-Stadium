"""Tests for the Feedback module."""


def test_submit_feedback(client):
    response = client.post(
        "/api/v1/feedback",
        json={"visitor_name": "John Doe", "category": "general", "rating": 5, "comments": "Great experience!"},
    )
    assert response.status_code == 201
    assert response.json()["data"]["rating"] == 5


def test_invalid_rating_fails_validation(client):
    response = client.post(
        "/api/v1/feedback", json={"visitor_name": "John Doe", "rating": 7}
    )
    assert response.status_code == 422


def test_feedback_average_summary(client):
    client.post("/api/v1/feedback", json={"visitor_name": "A", "rating": 4})
    client.post("/api/v1/feedback", json={"visitor_name": "B", "rating": 2})
    response = client.get("/api/v1/feedback/summary")
    assert response.status_code == 200
    assert response.json()["data"]["average_rating"] == 3.0
    assert response.json()["data"]["total_responses"] == 2
