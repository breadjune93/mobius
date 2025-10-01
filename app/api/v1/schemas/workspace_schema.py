from datetime import datetime
from pydantic import BaseModel, Field

class WorkspaceResponse(BaseModel):
    id: int
    title: str
    description: str
    goal: str
    owner: str
    user_count: int
    agent_count: int
    created_at: datetime

class GetWorkspacesRequest(BaseModel):
    user_id: str = Field(max_length=50)

class GetWorkspacesResponse(BaseModel):
    workspaces: list[WorkspaceResponse]

class GetWorkspaceRequest(BaseModel):
    workspace_id: int = Field()

class GetWorkspaceResponse(BaseModel):
    workspace: WorkspaceResponse

class CreateWorkspace(BaseModel):
    title: str = Field(max_length=100)
    description: str = Field(max_length=255, default="")
    type: str = Field(max_length=50, default="general")  # frontend에서 type으로 전송
    owner: str = Field(max_length=50, default="")  # JWT에서 추출 예정

class UpdateWorkspace(BaseModel):
    title: str = Field(max_length=100)
    description: str = Field(max_length=255)
    goal: str = Field(max_length=50, default="NORMAL")

class DeleteWorkspace(BaseModel):
    id: int = Field()
    owner: str = Field(max_length=50)

class ResultResponse(BaseModel):
    is_succeed: bool = True