from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.core.security import verify_access_token, SecurityError, decode_token, verify_refresh_token
from app.db.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", auto_error=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_subject(request: Request, token: str = Depends(oauth2_scheme)) -> str:
    # print(f"user_id 확인: {request.state.user_id}")
    # 1. middleware에서 설정한 request.state.user_id를 우선 확인
    if request.session["user_id"] is not None:
        return request.session["user_id"]

    # 2. OAuth2 토큰이 있으면 decode
    if token:
        try:
            user_id = decode_token(token).get("sub")
            print(f"OAuth2 토큰에서 user_id 추출: {user_id}")
            return user_id
        except SecurityError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    # 3. 둘 다 없으면 인증 실패
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication credentials were missing or invalid."
    )