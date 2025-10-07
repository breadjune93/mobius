from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class Chats(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), ForeignKey("sessions.id"), nullable=False)
    send_type = Column(String(50), nullable=False)
    send_id = Column(String(50), nullable=False)
    send_name = Column(String(50), nullable=True)
    chat_type = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    execution_status = Column(String(50), default="completed", nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
