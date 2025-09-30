from sqlalchemy import Column, DateTime, String, Integer, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "access"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    token = Column(String(150), unique=True, nullable=False)
    expired_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
