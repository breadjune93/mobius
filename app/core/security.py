import bcrypt
from datetime import datetime, timezone, timedelta
from app.core.config import settings
from jose import jwt
from sqlalchemy.orm import Session
from app.db.models.user import User

from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError

class SecurityError(Exception):
    pass

def hash_password(plain: str) -> str:
    salt = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
    return bcrypt.hashpw(plain.encode(), salt).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_access_token(subject: str, minutes: int = 30) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(minutes=minutes),
        "typ": "access",
    }
    return jwt.encode(payload, settings.SECRET, algorithm=settings.JWT_ALG)

def create_refresh_token(subject: str, days: int = 7) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(days=days),
        "typ": "refresh",
    }
    return jwt.encode(payload, settings.SECRET, algorithm=settings.JWT_ALG)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET, algorithms=[settings.JWT_ALG])

def verify_access_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, settings.SECRET, algorithms=[settings.JWT_ALG])
        if payload.get("typ") != "access" or not payload.get("sub"):
            return False

        return True
    except Exception:
        return False

def verify_refresh_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, settings.SECRET, algorithms=[settings.JWT_ALG])
        if payload.get("typ") != "refresh" or not payload.get("sub"):
            return False

        # try:
        #     user = db.query(User).filter(User.id == payload.get("sub")).first()
        # finally:
        #     db.close()
        #
        # if not user or user.refresh_token != token or not user.is_active:
        #     return False

        return True
    except Exception:
        return False
