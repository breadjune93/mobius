from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List


# ============================================
# PylonAgents Schemas
# ============================================
class PylonAgentsResponse(BaseModel):
    id: int
    pylon_id: int
    agent_id: str
    agent_image_url: str
    session_id: Optional[str] = None
    session_state: str
    working_directory: str
    claude_md_content: Optional[str] = None
    mcp_servers: Optional[dict] = None
    subagents_enabled: bool
    active_subagents: Optional[dict] = None
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


class GetPylonAgentsResponse(BaseModel):
    pylon_agents: List[PylonAgentsResponse]


class GetPylonAgentResponse(BaseModel):
    pylon_agent: PylonAgentsResponse


class CreatePylonAgentRequest(BaseModel):
    pylon_id: int = Field(description="파일런 ID")
    agent_id: str = Field(max_length=255, description="에이전트 ID")
    agent_image_url: str = Field(max_length=255, description="에이전트 이미지 URL")
    working_directory: str = Field(max_length=500, description="작업 디렉토리")
    session_id: Optional[str] = Field(default=None, max_length=255, description="세션 ID")
    session_state: str = Field(default="active", max_length=50, description="세션 상태")
    claude_md_content: Optional[str] = Field(default=None, description="Claude MD 내용")
    mcp_servers: Optional[dict] = Field(default=None, description="MCP 서버 설정")
    subagents_enabled: bool = Field(default=False, description="서브 에이전트 활성화")
    active_subagents: Optional[dict] = Field(default=None, description="활성 서브 에이전트")
    memory_enabled: bool = Field(default=False, description="메모리 활성화")
    memory_directory: Optional[str] = Field(default=None, max_length=255, description="메모리 디렉토리")
    allowed_tools: Optional[dict] = Field(default=None, description="허용된 도구")
    disallowed_tools: Optional[dict] = Field(default=None, description="비허용 도구")


class UpdatePylonAgentRequest(BaseModel):
    agent_image_url: Optional[str] = Field(default=None, max_length=255, description="에이전트 이미지 URL")
    session_id: Optional[str] = Field(default=None, max_length=255, description="세션 ID")
    session_state: Optional[str] = Field(default=None, max_length=50, description="세션 상태")
    working_directory: Optional[str] = Field(default=None, max_length=500, description="작업 디렉토리")
    claude_md_content: Optional[str] = Field(default=None, description="Claude MD 내용")
    mcp_servers: Optional[dict] = Field(default=None, description="MCP 서버 설정")
    subagents_enabled: Optional[bool] = Field(default=None, description="서브 에이전트 활성화")
    active_subagents: Optional[dict] = Field(default=None, description="활성 서브 에이전트")
    memory_enabled: Optional[bool] = Field(default=None, description="메모리 활성화")
    memory_directory: Optional[str] = Field(default=None, max_length=255, description="메모리 디렉토리")
    allowed_tools: Optional[dict] = Field(default=None, description="허용된 도구")
    disallowed_tools: Optional[dict] = Field(default=None, description="비허용 도구")


class UpdatePylonAgentStatsRequest(BaseModel):
    tokens_used: int = Field(default=0, description="사용된 토큰 수")
    tool_calls: int = Field(default=0, description="도구 호출 수")
    turns_completed: int = Field(default=0, description="완료된 턴 수")
    response_time: Optional[int] = Field(default=None, description="응답 시간 (ms)")
