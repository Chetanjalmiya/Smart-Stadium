"""Tests for the AI Fan Assistant module."""


def _create_faq(client, **overrides):
    payload = {
        "keywords": "parking cost price fee",
        "question": "How much does parking cost?",
        "answer": "Parking costs $5 per hour.",
        "category": "parking",
    }
    payload.update(overrides)
    return client.post("/api/v1/assistant/faq", json=payload)


def test_create_faq_entry(client):
    response = _create_faq(client)
    assert response.status_code == 201
    assert response.json()["data"]["category"] == "parking"


def test_ask_assistant_matches_faq(client):
    _create_faq(client)
    response = client.post("/api/v1/assistant/ask", json={"query": "how much is parking"})
    assert response.status_code == 200
    body = response.json()["data"]
    assert body["matched"] is True
    assert "5" in body["answer"]


def test_ask_assistant_no_match_returns_fallback(client):
    response = client.post("/api/v1/assistant/ask", json={"query": "xyzzyzz unrelated gibberish query"})
    assert response.status_code == 200
    body = response.json()["data"]
    assert body["matched"] is False


def test_chat_history_recorded(client):
    _create_faq(client)
    client.post("/api/v1/assistant/ask", json={"query": "parking cost"})
    response = client.get("/api/v1/assistant/history")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
