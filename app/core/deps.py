from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.core.security import decode_token
from app.db.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
#     try:
#         payload = decode_token(token)
#         if payload.get("type") != "access":
#             raise HTTPException(status_code=401, detail="유효하지 않은 액세스 토큰")
#         user_id = payload.get("sub")
#         user = db.query(User).get(user_id)
#         if not user or not user.is_active:
#             raise HTTPException(status_code=401, detail="비활성 사용자거나 존재하지 않음")
#         return user
#     except Exception:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰 검증 실패")