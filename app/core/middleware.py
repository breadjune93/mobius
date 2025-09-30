from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable, Any
from sqlalchemy.orm import Session
from app.core.security import decode_token, verify_access_token
from app.db.base import SessionLocal
from app.db.models.user import User


def _verify_refresh_token(token: str, db: Session) -> Any | None:
    """Refresh token 검증 (DB 저장된 토큰과 비교)"""
    try:
        payload = decode_token(token)

        if payload.get("typ") != "refresh":
            return None

        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()

        if not user or user.refresh_token != token or not user.is_active:
            return None

        return user_id
    except Exception as e:
        print(f"refresh token exception: {e}")
        return None

class AuthMiddleware(BaseHTTPMiddleware):
    """
    JWT 토큰 기반 인증 미들웨어
    Authorization 헤더의 Bearer 토큰과 쿠키의 refresh_token을 검증
    """

    def __init__(self, app, protected_paths: list = None, public_paths: list = None):
        super().__init__(app)
        self.protected_paths = protected_paths or []
        self.public_paths = public_paths or []

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        path = request.url.path
        print(f"dispatch 호출 - {request.method} {path}")

        # 공개 경로는 인증 체크 없이 통과
        if any(path.startswith(public_path) for public_path in self.public_paths):
            return await call_next(request)

        # API 경로와 일반 웹 경로 구분
        is_api_path = path.startswith("/api/")

        # 보호된 경로에 대해서만 인증 체크
        if any(path.startswith(protected_path) for protected_path in self.protected_paths):
            user_id = None

            # 1. Authorization 헤더에서 Bearer 토큰 확인
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                access_token = auth_header.split(" ")[1]
                user_id = verify_access_token(access_token)

            # 2. Access token이 유효하지 않으면 refresh token으로 검증
            if not user_id:
                refresh_token = request.cookies.get("refresh_token")
                if refresh_token:
                    db = SessionLocal()
                    try:
                        user_id = _verify_refresh_token(refresh_token, db)
                    finally:
                        db.close()

            # 3. 인증 실패 처리
            if not user_id:
                if is_api_path or request.headers.get("content-type") == "application/json":
                    # API 요청은 401 에러 반환
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="인증이 필요합니다."
                    )
                else:
                    # 웹 페이지 요청은 로그인 페이지로 리다이렉트
                    redirect = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
                    redirect.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
                    return redirect

            # 4. 인증된 사용자 정보를 request state에 저장
            request.state.user_id = user_id

        response = await call_next(request)

        # 캐시 방지 헤더 추가
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        return response