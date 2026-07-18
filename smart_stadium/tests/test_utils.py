"""Unit tests for utility modules that don't require the HTTP client."""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.utils.qrcode_util import generate_ticket_code, generate_qr_code_base64
from app.utils.exceptions import NotFoundException, ValidationException, ConflictException, UnauthorizedException
from app.utils.responses import success_response
from app.services.crowd_service import classify_risk


def test_generate_ticket_code_format():
    code = generate_ticket_code()
    assert code.startswith("TCKT-")
    assert len(code) == 17


def test_generate_ticket_code_unique():
    codes = {generate_ticket_code() for _ in range(20)}
    assert len(codes) == 20


def test_generate_qr_code_base64_format():
    qr = generate_qr_code_base64("TCKT-ABC123")
    assert qr.startswith("data:image/png;base64,")
    assert len(qr) > 100


def test_not_found_exception_message_and_status():
    exc = NotFoundException("Ticket", 42)
    assert exc.status_code == 404
    assert "Ticket" in exc.message
    assert "42" in exc.message


def test_validation_exception_status():
    exc = ValidationException("Invalid input")
    assert exc.status_code == 422


def test_conflict_exception_status():
    exc = ConflictException("Already exists")
    assert exc.status_code == 409


def test_unauthorized_exception_default_message():
    exc = UnauthorizedException()
    assert exc.status_code == 401
    assert exc.message == "Unauthorized access."


def test_success_response_default_values():
    response = success_response()
    assert response["success"] is True
    assert response["data"] is None


def test_success_response_with_data():
    response = success_response(data={"id": 1}, message="Created")
    assert response["data"] == {"id": 1}
    assert response["message"] == "Created"


def test_classify_risk_levels():
    assert classify_risk(95) == "critical"
    assert classify_risk(80) == "high"
    assert classify_risk(60) == "moderate"
    assert classify_risk(20) == "normal"
