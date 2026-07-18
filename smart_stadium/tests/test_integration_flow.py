"""End-to-end integration test simulating a real fan's stadium visit journey."""
from datetime import datetime, timedelta


def test_full_fan_journey(client, admin_headers):
    # 1. Admin schedules a match.
    match_resp = client.post(
        "/api/v1/matches",
        json={
            "home_team": "Falcons FC",
            "away_team": "Eagles United",
            "scheduled_time": (datetime.utcnow() + timedelta(hours=2)).isoformat(),
        },
    )
    assert match_resp.status_code == 201
    match = match_resp.json()["data"]

    # 2. Fan buys a ticket, receives a QR code.
    ticket_resp = client.post(
        "/api/v1/tickets",
        json={
            "match_id": match["id"],
            "holder_name": "Sam Fan",
            "holder_email": "sam@example.com",
            "seat_number": "A1-1",
            "price": 45.0,
        },
    )
    assert ticket_resp.status_code == 201
    ticket = ticket_resp.json()["data"]
    assert ticket["qr_code_data"] is not None

    # 3. Fan checks in at the gate using the QR ticket code.
    checkin_resp = client.post("/api/v1/tickets/verify", json={"ticket_code": ticket["ticket_code"]})
    assert checkin_resp.status_code == 200
    assert checkin_resp.json()["data"]["status"] == "used"

    # 4. Fan asks the AI assistant where the restroom is.
    client.post(
        "/api/v1/assistant/faq",
        json={
            "keywords": "restroom toilet washroom",
            "question": "Where is the restroom?",
            "answer": "Restrooms are in the North and South wings.",
            "category": "navigation",
        },
    )
    ask_resp = client.post("/api/v1/assistant/ask", json={"query": "where is the restroom"})
    assert ask_resp.status_code == 200
    assert ask_resp.json()["data"]["matched"] is True

    # 5. Fan books a parking slot.
    slot_resp = client.post(
        "/api/v1/parking/slots", json={"slot_number": "P1-01", "zone": "P1", "hourly_rate": 5.0}
    )
    slot = slot_resp.json()["data"]
    booking_resp = client.post(
        "/api/v1/parking/bookings",
        json={"slot_id": slot["id"], "vehicle_number": "XYZ-999", "visitor_name": "Sam Fan"},
    )
    assert booking_resp.status_code == 201

    # 6. Fan orders food.
    menu_resp = client.post(
        "/api/v1/food/menu",
        json={"name": "Burger", "category": "Main Course", "price": 8.0, "stall_location": "Stall 1"},
    )
    menu_item = menu_resp.json()["data"]
    order_resp = client.post(
        "/api/v1/food/orders",
        json={
            "customer_name": "Sam Fan",
            "seat_number": "A1-1",
            "items": [{"menu_item_id": menu_item["id"], "quantity": 2}],
        },
    )
    assert order_resp.status_code == 201
    assert order_resp.json()["data"]["total_amount"] == 16.0

    # 7. Crowd density is recorded for the section.
    crowd_resp = client.post(
        "/api/v1/crowd", json={"zone": "Section A", "current_count": 400, "capacity": 500}
    )
    assert crowd_resp.status_code == 201
    assert crowd_resp.json()["data"]["risk_level"] == "high"

    # 8. Fan leaves feedback after the match.
    feedback_resp = client.post(
        "/api/v1/feedback",
        json={"visitor_name": "Sam Fan", "category": "general", "rating": 5, "comments": "Amazing day!"},
    )
    assert feedback_resp.status_code == 201

    # 9. Admin reviews the full dashboard.
    dashboard_resp = client.get("/api/v1/admin/dashboard", headers=admin_headers)
    assert dashboard_resp.status_code == 200
    dashboard = dashboard_resp.json()["data"]
    assert dashboard["tickets"]["total_checked_in"] == 1
    assert dashboard["food"]["total_orders"] == 1
    assert dashboard["parking"]["occupied_slots"] == 1
