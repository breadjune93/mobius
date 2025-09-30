from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func
from app.db.base import Base

class Workspaces(Base):
    __tablename__ = "workspaces"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    goal = Column(String(50), nullable=False, default="NORMAL")
    owner = Column(String(50), nullable=False)
    user_count = Column(Integer, nullable=False, default="1")
    agent_count = Column(Integer, nullable=False, default="0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
