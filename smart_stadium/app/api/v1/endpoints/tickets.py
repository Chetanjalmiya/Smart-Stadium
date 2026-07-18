"""API routes for the Smart Ticket (QR Code) module."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.ticket_service import TicketService
from app.schemas.ticket import TicketCreate, TicketResponse, TicketVerifyRequest
from app.utils.responses import success_response

router = APIRouter(prefix="/tickets", tags=["Smart Ticket (QR Code)"])


@router.post("", response_model=dict, status_code=201, summary="Issue a new ticket with QR code")
def issue_ticket(payload: TicketCreate, db: Session = Depends(get_db)) -> dict:
    ticket = TicketService(db).issue_ticket(payload)
    return success_response(TicketResponse.model_validate(ticket).model_dump(), "Ticket issued successfully.")


@router.get("", response_model=dict, summary="List all tickets")
def list_tickets(match_id: Optional[int] = Query(default=None), db: Session = Depends(get_db)) -> dict:
    tickets = TicketService(db).list_tickets(match_id)
    data = [TicketResponse.model_validate(t).model_dump() for t in tickets]
    return success_response(data, f"Retrieved {len(data)} ticket(s).")


@router.get("/{ticket_id}", response_model=dict, summary="Get ticket by ID")
def get_ticket(ticket_id: int, db: Session = Depends(get_db)) -> dict:
    ticket = TicketService(db).get_ticket(ticket_id)
    return success_response(TicketResponse.model_validate(ticket).model_dump())


@router.post("/verify", response_model=dict, summary="Verify a ticket QR code and check in")
def verify_ticket(payload: TicketVerifyRequest, db: Session = Depends(get_db)) -> dict:
    ticket = TicketService(db).verify_and_checkin(payload.ticket_code)
    return success_response(TicketResponse.model_validate(ticket).model_dump(), "Ticket verified and checked in.")


@router.post("/{ticket_id}/cancel", response_model=dict, summary="Cancel a ticket")
def cancel_ticket(ticket_id: int, db: Session = Depends(get_db)) -> dict:
    ticket = TicketService(db).cancel_ticket(ticket_id)
    return success_response(TicketResponse.model_validate(ticket).model_dump(), "Ticket cancelled successfully.")
