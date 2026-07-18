"""API routes for the AI Fan Assistant module."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.assistant_service import AssistantService
from app.schemas.faq import (
    FAQEntryCreate,
    FAQEntryResponse,
    AssistantQueryRequest,
    AssistantQueryResponse,
)
from app.utils.responses import success_response

router = APIRouter(prefix="/assistant", tags=["AI Fan Assistant"])


@router.post("/faq", response_model=dict, status_code=201, summary="Add a knowledge-base FAQ entry")
def create_faq(payload: FAQEntryCreate, db: Session = Depends(get_db)) -> dict:
    faq = AssistantService(db).create_faq(payload)
    return success_response(FAQEntryResponse.model_validate(faq).model_dump(), "FAQ entry created.")


@router.get("/faq", response_model=dict, summary="List FAQ entries")
def list_faqs(category: Optional[str] = Query(default=None), db: Session = Depends(get_db)) -> dict:
    faqs = AssistantService(db).list_faqs(category)
    data = [FAQEntryResponse.model_validate(f).model_dump() for f in faqs]
    return success_response(data, f"Retrieved {len(data)} FAQ entr(y/ies).")


@router.post("/ask", response_model=dict, summary="Ask the AI Fan Assistant a question")
def ask_assistant(payload: AssistantQueryRequest, db: Session = Depends(get_db)) -> dict:
    result: AssistantQueryResponse = AssistantService(db).ask(payload)
    return success_response(result.model_dump(), "Query processed.")


@router.get("/history", response_model=dict, summary="Get recent chat history")
def get_history(limit: int = Query(default=50, ge=1, le=200), db: Session = Depends(get_db)) -> dict:
    logs = AssistantService(db).get_chat_history(limit)
    data = [
        {
            "id": log.id,
            "query": log.user_query,
            "response": log.response,
            "created_at": log.created_at.isoformat(),
        }
        for log in logs
    ]
    return success_response(data, f"Retrieved {len(data)} chat log(s).")
