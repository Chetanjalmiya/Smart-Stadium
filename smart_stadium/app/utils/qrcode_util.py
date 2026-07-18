"""QR code generation utilities for Smart Ticket module."""
import base64
import io
import uuid
import qrcode


def generate_ticket_code() -> str:
    """Generate a unique ticket code."""
    return f"TCKT-{uuid.uuid4().hex[:12].upper()}"


def generate_qr_code_base64(data: str) -> str:
    """Generate a QR code PNG for the given data and return it as a base64 string."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"
