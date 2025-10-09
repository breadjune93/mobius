from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.base import Base

class Agents(Base):
    __tablename__ = "agents"

    id = Column(String(255), primary_key=True)
    name = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    assistant = Column(String(50), default="anthropic", nullable=False)
    model = Column(String(255), default="claude-sonnet-4-5", nullable=False)
    instructions = Column(Text, nullable=False)
    description = Column(String(255), nullable=False)
    max_turns = Column(Integer, default=50, nullable=False)
    temperature = Column(Numeric(3, 2), default=1.0, nullable=False)
    allowed_tools = Column(JSONB, nullable=True)
    disallowed_tools = Column(JSONB, nullable=True)
    mcp_servers = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
