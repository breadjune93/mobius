from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.base import Base

class PylonAgents(Base):
    __tablename__ = "pylon_agents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pylon_id = Column(Integer, ForeignKey("pylons.id"), nullable=False)
    agent_id = Column(String(255), nullable=False)
    agent_image_url = Column(String(255), nullable=False)
    session_id = Column(String(255), nullable=True)
    session_state = Column(String(50), default="active", nullable=False)
    working_directory = Column(String(500), nullable=False)
    claude_md_content = Column(Text, nullable=True)
    mcp_servers = Column(JSONB, nullable=True)
    subagents_enabled = Column(Boolean, default=False, nullable=False)
    active_subagents = Column(JSONB, nullable=True)
    memory_enabled = Column(Boolean, default=False, nullable=False)
    memory_directory = Column(String(255), nullable=True)
    allowed_tools = Column(JSONB, nullable=True)
    disallowed_tools = Column(JSONB, nullable=True)
    total_tokens_used = Column(BigInteger, default=0, nullable=False)
    total_tool_calls = Column(Integer, default=0, nullable=False)
    total_turns_completed = Column(Integer, default=0, nullable=False)
    average_response_time = Column(Integer, nullable=True)
    last_checkpoint_at = Column(DateTime(timezone=True), nullable=True)
    checkpoint_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
