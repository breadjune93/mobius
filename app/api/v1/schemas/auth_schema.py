from pydantic import BaseModel, Field
from typing import Optional

class SignupRequest(BaseModel):
    user_id: str = Field(min_length=3, max_length=50)
    username: str = Field()
    password: str = Field(min_length=6, max_length=128)
    theme: Optional[str] = Field(default="DARK")

class LoginRequest(BaseModel):
    user_id: str
    password: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class ResultResponse(BaseModel):
    is_succeed: bool = True