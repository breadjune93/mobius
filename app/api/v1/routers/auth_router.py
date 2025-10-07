from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.api.v1.schemas.auth_schema import SignupRequest, LoginRequest, ResultResponse, TokenPair
from app.api.v1.services.auth_service import AuthService
from app.db.repositories.user_repository import UserRepository
from app.db.repositories.setting_repository import SettingRepository

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
service = AuthService(UserRepository(), SettingRepository())

@router.post("/signup", response_model=ResultResponse)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    data = service.signup(db, payload.user_id, payload.username, payload.password, payload.theme)
    return ResultResponse(**data)

@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    data = service.login(db, payload.user_id, payload.password)

    # refresh_token을 httpOnly 쿠키로 설정
    response.set_cookie(
        key="refresh_token",
        value=data["refresh_token"],
        httponly=True,
        secure=True,  # HTTPS에서만 전송
        samesite="strict",  # CSRF 보호
        max_age=7 * 24 * 60 * 60  # 7일
    )

    return TokenPair(**data)