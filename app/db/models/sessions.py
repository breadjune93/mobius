from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.base import Base

class Sessions(Base):
    __tablename__ = "sessions"

    id = Column(String(255), primary_key=True)
    pylon_id = Column(Integer, ForeignKey("pylons.id"), nullable=False)
    agent_id = Column(String(255), ForeignKey("agents.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=True)
    session_state = Column(String(50), default="active", nullable=True)
    working_directory = Column(String(500), nullable=False)
    fork_id = Column(String(255), nullable=True)
    claude_md_content = Column(Text, nullable=True)
    mcp_servers = Column(JSONB, nullable=True)
    subagents_enabled = Column(Boolean, default=False, nullable=True)
    active_subagents = Column(JSONB, nullable=True)
    context_token_count = Column(Integer, default=0, nullable=True)
    memory_enabled = Column(Boolean, default=False, nullable=True)
    memory_directory = Column(String(255), nullable=True)
    allowed_tools = Column(JSONB, nullable=True)
    disallowed_tools = Column(JSONB, nullable=True)
    total_tokens_used = Column(BigInteger, default=0, nullable=True)
    total_tool_calls = Column(Integer, default=0, nullable=True)
    total_turns_completed = Column(Integer, default=0, nullable=True)
    average_response_time = Column(Integer, nullable=True)
    last_checkpoint_at = Column(DateTime(timezone=True), nullable=True)
    checkpoint_count = Column(Integer, default=0, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
