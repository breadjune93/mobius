from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable, Any
from sqlalchemy.orm import Session
from app.core.security import decode_token, verify_access_token, verify_refresh_token, create_access_token, create_refresh_token
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
        new_access_token = None
        new_refresh_token = None

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
                    # 리프레시 토큰 인증 성공 - 토큰 재발급
                    user = decode_token(refresh_cookies)
                    user_id = user.get("sub")
                    print(f"리프레시 토큰 인증 성공 - 사용자 ID: {user_id}")

                    # 새로운 access_token과 refresh_token 생성
                    new_access_token = create_access_token(user_id)
                    new_refresh_token = create_refresh_token(user_id)

                    # DB에 새로운 refresh_token 저장
                    db = SessionLocal()
                    try:
                        db_user = db.query(User).filter(User.id == user_id).first()
                        if db_user:
                            db_user.refresh_token = new_refresh_token
                            db.commit()
                            print(f"새로운 refresh_token DB 저장 완료")
                    finally:
                        db.close()
            else:
                user = decode_token(authorization_header.split(" ")[1])
                print(f"엑세스 토큰 인증 성공: {user}")

        # 인증된 사용자 정보를 request.state에 저장
        if user:
            request.session["user_id"] = user.get("sub")
            # request.state.user_id = user.get("sub")
            # print(f"request.state.user_id 설정: {request.state.user_id}")

        response = await call_next(request)

        # 토큰이 재발급된 경우 response에 설정
        if new_access_token:
            # access_token을 response header에 추가
            response.headers["X-New-Access-Token"] = new_access_token
            print(f"새로운 access_token을 응답 헤더에 추가")

        if new_refresh_token:
            # refresh_token을 httpOnly 쿠키로 설정
            response.set_cookie(
                key="mb_an_tk",
                value=new_refresh_token,
                httponly=True,
                secure=True,
                samesite="strict",
                max_age=7 * 24 * 60 * 60  # 7일
            )
            print(f"새로운 refresh_token을 쿠키에 설정")

        # 캐시 방지 헤더 추가
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        return response