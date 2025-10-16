from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List


# ============================================
# Agent Schemas
# ============================================
class AgentResponse(BaseModel):
    id: str
    name: str
    is_active: bool
    assistant: str
    model: str
    instructions: str
    description: str
    max_turns: int
    temperature: float
    allowed_tools: Optional[dict] = None
    disallowed_tools: Optional[dict] = None
    mcp_servers: Optional[dict] = None
    created_at: datetime
    updated_at: datetime


class GetAgentsResponse(BaseModel):
    agents: List[AgentResponse]


class GetAgentResponse(BaseModel):
    agent: AgentResponse


# ============================================
# Chat Schemas
# ============================================
class ChatResponse(BaseModel):
    id: int
    session_id: str
    send_type: str
    send_id: str
    send_name: Optional[str] = None
    chat_type: str
    message: str
    execution_status: str
    created_at: datetime


class GetChatsResponse(BaseModel):
    chats: List[ChatResponse]


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, description="채팅 메시지")


class CreateChatRequest(BaseModel):
    session_id: str = Field(description="세션 ID")
    send_type: str = Field(description="발신자 유형 (user/agent/system)")
    send_id: str = Field(description="발신자 ID")
    send_name: Optional[str] = Field(default=None, description="발신자 이름")
    chat_type: str = Field(description="채팅 타입 (text/tool/error)")
    message: str = Field(description="메시지 내용")
    execution_status: str = Field(default="completed", description="실행 상태")


# ============================================
# Common Response
# ============================================
class ResultResponse(BaseModel):
    is_succeed: bool = True
    message: Optional[str] = None
