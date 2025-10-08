from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.core.security import verify_access_token, SecurityError, decode_token, verify_refresh_token
from app.db.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_subject(token: str = Depends(oauth2_scheme)) -> str:
    try:
        if not verify_access_token(token) and not verify_refresh_token(token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 액세스 토큰")

        return decode_token(token).get("sub")
        # if payload.get("type") != "access":
        #     raise HTTPException(status_code=401, detail="유효하지 않은 액세스 토큰")
        # user_id = payload.get("sub")
        # user = db.query(User).get(user_id)
        # if not user or not user.is_active:
        #     raise HTTPException(status_code=401, detail="비활성 사용자거나 존재하지 않음")
        # return user
    except SecurityError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))