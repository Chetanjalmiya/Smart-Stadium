"""Tests for the Smart Ticket (QR Code) module."""
from datetime import datetime, timedelta


def _create_match(client):
    payload = {
        "home_team": "Falcons FC",
        "away_team": "Eagles United",
        "scheduled_time": (datetime.utcnow() + timedelta(days=1)).isoformat(),
    }
    return client.post("/api/v1/matches", json=payload).json()["data"]


def _issue_ticket(client, match_id, **overrides):
    payload = {
        "match_id": match_id,
        "holder_name": "John Doe",
        "holder_email": "john@example.com",
        "seat_number": "A1-1",
        "price": 50.0,
    }
    payload.update(overrides)
    return client.post("/api/v1/tickets", json=payload)


def test_issue_ticket_generates_qr_code(client):
    match = _create_match(client)
    response = _issue_ticket(client, match["id"])
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["ticket_code"].startswith("TCKT-")
    assert body["qr_code_data"].startswith("data:image/png;base64,")
    assert body["status"] == "valid"


def test_issue_ticket_invalid_match_fails(client):
    response = _issue_ticket(client, 9999)
    assert response.status_code == 404


def test_issue_ticket_invalid_email_fails_validation(client):
    match = _create_match(client)
    response = _issue_ticket(client, match["id"], holder_email="not-an-email")
    assert response.status_code == 422


def test_verify_ticket_checkin_success(client):
    match = _create_match(client)
    ticket = _issue_ticket(client, match["id"]).json()["data"]
    response = client.post("/api/v1/tickets/verify", json={"ticket_code": ticket["ticket_code"]})
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "used"


def test_verify_ticket_twice_fails(client):
    match = _create_match(client)
    ticket = _issue_ticket(client, match["id"]).json()["data"]
    client.post("/api/v1/tickets/verify", json={"ticket_code": ticket["ticket_code"]})
    response = client.post("/api/v1/tickets/verify", json={"ticket_code": ticket["ticket_code"]})
    assert response.status_code == 409


def test_cancel_ticket(client):
    match = _create_match(client)
    ticket = _issue_ticket(client, match["id"]).json()["data"]
    response = client.post(f"/api/v1/tickets/{ticket['id']}/cancel")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "cancelled"


def test_list_tickets_filtered_by_match(client):
    match = _create_match(client)
    _issue_ticket(client, match["id"])
    _issue_ticket(client, match["id"], holder_email="jane@example.com")
    response = client.get(f"/api/v1/tickets?match_id={match['id']}")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2
