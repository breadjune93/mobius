from sqlalchemy import Column, DateTime, String, Integer, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String(50), primary_key=True)
    role_id = Column(Integer, nullable=False, default=1000)  # 일반 사용자 기본값
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)  # 사용자 활성 상태
    refresh_token = Column(String(50), unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())