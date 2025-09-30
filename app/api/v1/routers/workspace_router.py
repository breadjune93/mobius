from fastapi import APIRouter, Depends, HTTPException, Header, Response
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.api.v1.schemas.auth_schema import SignupRequest, LoginRequest, ResultResponse, TokenPair
from app.api.v1.services.auth_service import AuthService
from app.db.repositories.user_repository import UserRepository
from app.db.repositories.setting_repository import SettingRepository

router = APIRouter(prefix="/api/v1/nexus", tags=["nexus"])
service = AuthService(UserRepository(), SettingRepository())

# 워크스페이스 리스트 조회
@router.get("/workspaces", response_model=ResultResponse)
def get_workspaces(payload: SignupRequest, db: Session = Depends(get_db)):
    data = service.signup(db, payload.user_id, payload.username, payload.password, payload.theme)
    return ResultResponse(**data)

# 워크스페이스 조회
@router.get("/workspace/{workspace_id}", response_model=TokenPair)
def get_workspace():
    return

# 워크스페이스 생성
@router.post("/workspace", response_model=TokenPair)
def create_workspace():
    return

# 워크스페이스 업데이트
@router.put("/workspace", response_model=TokenPair)
def update_workspace():
    return

# 워크스페이스 삭제
@router.delete("/workspace", response_model=TokenPair)
def delete_workspace():
    return

