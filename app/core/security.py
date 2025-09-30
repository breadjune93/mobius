import bcrypt
from datetime import datetime, timedelta
from app.core.config import settings
from jose import jwt

def hash_password(plain: str) -> str:
    salt = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
    return bcrypt.hashpw(plain.encode(), salt).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_access_token(sub: str) -> str:
    exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": sub, "exp": exp, "type": "access"}
    return jwt.encode(payload, settings.SECRET, algorithm=settings.JWT_ALG)

def create_refresh_token(sub: str) -> str:
    exp = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": sub, "exp": exp, "type": "refresh"}
    return jwt.encode(payload, settings.SECRET, algorithm=settings.JWT_ALG)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET, algorithms=[settings.JWT_ALG])

# 토큰 블랙리스트 (실제 운영환경에서는 Redis 등 외부 저장소 사용 권장)
_token_blacklist = set()

def delete_token(token: str) -> dict:
    """
    토큰을 무효화(블랙리스트에 추가)
    JWT는 stateless하므로 서버에서 토큰을 완전히 삭제할 수 없지만,
    블랙리스트를 통해 무효화된 토큰을 추적할 수 있음
    """
    try:
        # 토큰 검증 후 블랙리스트에 추가
        decoded = decode_token(token)
        _token_blacklist.add(token)
        return {
            "message": "토큰이 무효화되었습니다",
            "user_id": decoded.get("sub"),
            "token_type": decoded.get("type")
        }
    except Exception as e:
        raise ValueError(f"유효하지 않은 토큰: {str(e)}")

def is_token_blacklisted(token: str) -> bool:
    """
    토큰이 블랙리스트에 있는지 확인
    """
    return token in _token_blacklist

def verify_token_not_blacklisted(token: str) -> bool:
    """
    토큰이 블랙리스트에 없는지 확인하고 디코드
    """
    if is_token_blacklisted(token):
        raise ValueError("무효화된 토큰입니다")
    return True
