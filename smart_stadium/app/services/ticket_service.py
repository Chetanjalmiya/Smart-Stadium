"""Business logic for the Smart Ticket (QR Code) module."""
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.ticket import Ticket, TicketStatus
from app.models.match import Match
from app.schemas.ticket import TicketCreate
from app.utils.exceptions import NotFoundException, ConflictException
from app.utils.qrcode_util import generate_ticket_code, generate_qr_code_base64


class TicketService:
    """Encapsulates ticket issuance, QR generation, and check-in logic."""

    def __init__(self, db: Session):
        self.db = db

    def issue_ticket(self, payload: TicketCreate) -> Ticket:
        match = self.db.query(Match).filter(Match.id == payload.match_id).first()
        if not match:
            raise NotFoundException("Match", payload.match_id)

        ticket_code = generate_ticket_code()
        ticket = Ticket(ticket_code=ticket_code, **payload.model_dump())
        ticket.qr_code_data = generate_qr_code_base64(ticket_code)

        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def get_ticket(self, ticket_id: int) -> Ticket:
        ticket = self.db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise NotFoundException("Ticket", ticket_id)
        return ticket

    def get_by_code(self, ticket_code: str) -> Ticket:
        ticket = self.db.query(Ticket).filter(Ticket.ticket_code == ticket_code).first()
        if not ticket:
            raise NotFoundException("Ticket", ticket_code)
        return ticket

    def list_tickets(self, match_id: int | None = None) -> List[Ticket]:
        query = self.db.query(Ticket)
        if match_id:
            query = query.filter(Ticket.match_id == match_id)
        return query.order_by(Ticket.created_at.desc()).all()

    def verify_and_checkin(self, ticket_code: str) -> Ticket:
        ticket = self.get_by_code(ticket_code)
        if ticket.status == TicketStatus.USED:
            raise ConflictException("This ticket has already been used for check-in.")
        if ticket.status == TicketStatus.CANCELLED:
            raise ConflictException("This ticket has been cancelled and is not valid.")

        ticket.status = TicketStatus.USED
        ticket.checked_in_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def cancel_ticket(self, ticket_id: int) -> Ticket:
        ticket = self.get_ticket(ticket_id)
        if ticket.status == TicketStatus.USED:
            raise ConflictException("A used ticket cannot be cancelled.")
        ticket.status = TicketStatus.CANCELLED
        self.db.commit()
        self.db.refresh(ticket)
        return ticket
