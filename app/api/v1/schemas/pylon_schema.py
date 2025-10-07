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
# Session Schemas
# ============================================
class SessionResponse(BaseModel):
    id: str
    pylon_id: int
    agent_id: str
    is_active: bool
    session_state: str
    working_directory: str
    fork_id: Optional[str] = None
    claude_md_content: Optional[str] = None
    mcp_servers: Optional[dict] = None
    subagents_enabled: bool
    active_subagents: Optional[dict] = None
    context_token_count: int
    memory_enabled: bool
    memory_directory: Optional[str] = None
    allowed_tools: Optional[dict] = None
    disallowed_tools: Optional[dict] = None
    total_tokens_used: int
    total_tool_calls: int
    total_turns_completed: int
    average_response_time: Optional[int] = None
    last_checkpoint_at: Optional[datetime] = None
    checkpoint_count: int
    created_at: datetime
    updated_at: datetime


class GetSessionResponse(BaseModel):
    session: SessionResponse


class CreateSessionRequest(BaseModel):
    pylon_id: int = Field(description="파일런 ID")
    agent_id: str = Field(description="에이전트 ID")
    working_directory: str = Field(max_length=500, description="작업 디렉토리")
    memory_enabled: bool = Field(default=False, description="메모리 활성화 여부")
    memory_directory: Optional[str] = Field(default=None, max_length=255, description="메모리 디렉토리")


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
