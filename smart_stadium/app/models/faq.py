"""AI Fan Assistant module models — FAQ knowledge base and chat logs."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database.base import Base


class FAQEntry(Base):
    """Represents a knowledge-base entry used to answer fan questions."""

    __tablename__ = "faq_entries"

    id = Column(Integer, primary_key=True, index=True)
    keywords = Column(String(255), nullable=False)
    question = Column(String(255), nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, default="general")
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatLog(Base):
    """Represents a logged interaction with the AI Fan Assistant."""

    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_query = Column(Text, nullable=False)
    matched_faq_id = Column(Integer, nullable=True)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
