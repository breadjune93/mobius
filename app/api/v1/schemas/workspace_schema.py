from pydantic import BaseModel, Field

class CreateWorkspace(BaseModel):
    title: str = Field(max_length=100)
    description: str = Field(max_length=255)
    goal: str = Field(max_length=50, default="NORMAL")
    owner: str = Field(max_length=50)
    user_count: int = Field(default=1)
    agent_count: int = Field(default=0)

class UpdateWorkspace(BaseModel):
    title: str = Field(max_length=100)
    description: str = Field(max_length=255)
    goal: str = Field(max_length=50, default="NORMAL")

class DeleteWorkspace(BaseModel):
    id: int = Field()
    owner: str = Field(max_length=50)

class ResultResponse(BaseModel):
    is_succeed: bool = True