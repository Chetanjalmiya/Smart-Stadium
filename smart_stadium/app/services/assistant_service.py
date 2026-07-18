"""Business logic for the AI Fan Assistant module.

Implements a real, working keyword-matching retrieval engine over the FAQ
knowledge base stored in SQLite (no external AI API dependency required).
"""
import re
from typing import List
from sqlalchemy.orm import Session
from app.models.faq import FAQEntry, ChatLog
from app.schemas.faq import FAQEntryCreate, AssistantQueryRequest, AssistantQueryResponse
from app.utils.exceptions import NotFoundException

FALLBACK_ANSWER = (
    "I'm sorry, I couldn't find a specific answer to that. "
    "Please check the Stadium Information section or contact a staff member for help."
)


def _tokenize(text: str) -> set:
    """Lowercase and split text into a set of alphanumeric tokens."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))


class AssistantService:
    """Encapsulates FAQ management and keyword-based query resolution."""

    def __init__(self, db: Session):
        self.db = db

    def create_faq(self, payload: FAQEntryCreate) -> FAQEntry:
        faq = FAQEntry(**payload.model_dump())
        self.db.add(faq)
        self.db.commit()
        self.db.refresh(faq)
        return faq

    def list_faqs(self, category: str | None = None) -> List[FAQEntry]:
        query = self.db.query(FAQEntry)
        if category:
            query = query.filter(FAQEntry.category == category)
        return query.order_by(FAQEntry.category.asc()).all()

    def get_faq(self, faq_id: int) -> FAQEntry:
        faq = self.db.query(FAQEntry).filter(FAQEntry.id == faq_id).first()
        if not faq:
            raise NotFoundException("FAQ entry", faq_id)
        return faq

    def ask(self, payload: AssistantQueryRequest) -> AssistantQueryResponse:
        """Resolve a natural-language fan query against the FAQ knowledge base."""
        query_tokens = _tokenize(payload.query)
        entries = self.db.query(FAQEntry).all()

        best_entry = None
        best_score = 0.0

        for entry in entries:
            keyword_tokens = _tokenize(entry.keywords)
            question_tokens = _tokenize(entry.question)
            entry_tokens = keyword_tokens | question_tokens
            if not entry_tokens or not query_tokens:
                continue
            overlap = query_tokens & entry_tokens
            score = len(overlap) / len(entry_tokens | query_tokens)
            if score > best_score:
                best_score = score
                best_entry = entry

        if best_entry and best_score >= 0.15:
            answer = best_entry.answer
            matched = True
            category = best_entry.category
            matched_id = best_entry.id
        else:
            answer = FALLBACK_ANSWER
            matched = False
            category = None
            matched_id = None
            best_score = 0.0

        log = ChatLog(user_query=payload.query, matched_faq_id=matched_id, response=answer)
        self.db.add(log)
        self.db.commit()

        return AssistantQueryResponse(
            query=payload.query,
            answer=answer,
            matched=matched,
            category=category,
            confidence=round(best_score, 2),
        )

    def get_chat_history(self, limit: int = 50) -> List[ChatLog]:
        return self.db.query(ChatLog).order_by(ChatLog.created_at.desc()).limit(limit).all()
