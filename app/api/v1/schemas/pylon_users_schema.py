from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List


# ============================================
# PylonUsers Schemas
# ============================================
class PylonUsersResponse(BaseModel):
    id: int
    pylon_id: int
    user_id: str
    user_role: str
    pylon_role: str
    user_image_url: str
    created_at: datetime
    updated_at: datetime


class GetPylonUsersResponse(BaseModel):
    pylon_users: List[PylonUsersResponse]


class GetPylonUserResponse(BaseModel):
    pylon_user: PylonUsersResponse


class CreatePylonUserRequest(BaseModel):
    pylon_id: int = Field(description="파일런 ID")
    user_id: str = Field(max_length=50, description="사용자 ID")
    user_role: str = Field(max_length=50, description="사용자 역할")
    pylon_role: str = Field(max_length=50, default="owner", description="파일런 내 역할")
    user_image_url: str = Field(max_length=255, description="사용자 이미지 URL")


class UpdatePylonUserRequest(BaseModel):
    user_role: Optional[str] = Field(default=None, max_length=50, description="사용자 역할")
    pylon_role: Optional[str] = Field(default=None, max_length=50, description="파일런 내 역할")
    user_image_url: Optional[str] = Field(default=None, max_length=255, description="사용자 이미지 URL")
