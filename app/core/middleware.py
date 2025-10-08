from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable, Any
from sqlalchemy.orm import Session
from app.core.security import decode_token, verify_access_token, verify_refresh_token
from app.db.base import SessionLocal
from app.db.models.user import User

def _is_authorization(header: str) -> bool:
    if not header or not header.startswith("Bearer "):
        return False

    access_token = header.split(" ")[1]
    if not verify_access_token(access_token):
        return False

    return True

def _verify_refresh_token(token: str) -> bool:
    db = SessionLocal()
    if not verify_refresh_token(token):
        return False

    try:
        payload = decode_token(token)
        user = db.query(User).filter(User.id == payload.get("sub")).first()
        if not user or user.refresh_token != token or not user.is_active:
            return False
    finally:
        db.close()

    return True

class AuthMiddleware(BaseHTTPMiddleware):

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

        user = None
        # 보호된 경로에 대해서만 인증 체크
        if any(path.startswith(protected_path) for protected_path in self.protected_paths):
            print("인증 시작")
            authorization_header = request.headers.get("Authorization")
            if not _is_authorization(authorization_header):
                print("엑세스 토큰 인증 실패")
                refresh_cookies = request.cookies.get("mb_an_tk")

                if not _verify_refresh_token(refresh_cookies):
                    print("리프레시 토큰 인증 실패")
                    if is_api_path or request.headers.get("content-type") == "application/json":
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication credentials were missing or invalid."
                        )
                    else:
                        redirect = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
                        redirect.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
                        return redirect
                else:
                    user = decode_token(refresh_cookies)
                    print(f"리프레시 토큰 인증 성공 {user}")
            else:
                user = decode_token(authorization_header.split(" ")[1])
                print(f"엑세스 토큰 인증 성공: {user}")


        # request.state.user_id = user.get("sub")

        response = await call_next(request)

        # 캐시 방지 헤더 추가
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        return response