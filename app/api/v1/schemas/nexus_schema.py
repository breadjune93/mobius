from datetime import datetime
from pydantic import BaseModel, Field

class PylonResponse(BaseModel):
    id: int
    title: str
    description: str
    goal: str
    owner: str
    user_count: int
    agent_count: int
    image_url: str = None
    created_at: datetime

class GetPylonsRequest(BaseModel):
    user_id: str = Field(max_length=50)

class GetPylonsResponse(BaseModel):
    pylons: list[PylonResponse]

class GetPylonRequest(BaseModel):
    pylon_id: int = Field()

class GetPylonResponse(BaseModel):
    pylon: PylonResponse

class CreatePylon(BaseModel):
    title: str = Field(max_length=100)
    description: str = Field(max_length=255, default="")
    type: str = Field(max_length=50, default="general")  # frontend에서 type으로 전송
    owner: str = Field(max_length=50, default="")  # JWT에서 추출 예정
    image_url: str = Field(max_length=500, default="")

class UpdatePylon(BaseModel):
    title: str = Field(max_length=100)
    description: str = Field(max_length=255)
    goal: str = Field(max_length=50, default="NORMAL")

class DeletePylon(BaseModel):
    id: int = Field()
    owner: str = Field(max_length=50)

class ResultResponse(BaseModel):
    is_succeed: bool = True
