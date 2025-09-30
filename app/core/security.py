import bcrypt
from datetime import datetime, timezone, timedelta
from app.core.config import settings
from jose import jwt
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

def verify_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET, algorithms=[settings.JWT_ALG])
        if payload.get("typ") != "access":
            raise SecurityError("유효하지 않은 액세스 토큰")
        sub = payload.get("sub")
        if not sub:
            raise SecurityError("사용자가 존재하지 않음")
        return sub
    except ExpiredSignatureError:
        raise SecurityError("토큰 만료")
    except JWTClaimsError or JWTError as e:
        # 클레임 불일치 또는 서명/형식/알고리즘 오류
        raise SecurityError(f"토큰 검증 실패: {e}")