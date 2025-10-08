import os
from typing import List

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.middleware import AuthMiddleware  # 세션을 읽는 인증 미들웨어
from app.db.base import Base, engine

# 웹 라우터(템플릿/세션 기반)
from web.routes.route import router as web_router

# API 라우터(v1, JSON)
from api.v1.routers.auth_router import router as auth_router
from api.v1.routers.nexus_router import router as nexus_router
from api.v1.routers.pylon_router import router as pylon_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Agent by Mobius",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # ─────────────────────────────────────────────────────────────────────
    # CORS
    # ─────────────────────────────────────────────────────────────────────
    # allowed_origins: List[str] = [
    #     "http://localhost:1993",
    #     "http://127.0.0.1:1993",
    #     # 운영 도메인 추가
    # ]

    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=allowed_origins,
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )

    app.add_middleware(
        AuthMiddleware,
        protected_paths=["/nexus", "/mission", "/api/v1/chat"],  # 보호된 경로들
        public_paths=["/signup", "/forgot-password", "/logout", "/css", "/js", "/image", "/api/v1/auth"]  # 공개 경로들
    )

    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET)

    # ─────────────────────────────────────────────────────────────────────
    # 정적 파일 mount (웹)
    # ─────────────────────────────────────────────────────────────────────
    app.mount("/image", StaticFiles(directory="web/static/image"), name="image")
    app.mount("/css", StaticFiles(directory="web/static/css"), name="css")
    app.mount("/js", StaticFiles(directory="web/static/js"), name="js")

    # ─────────────────────────────────────────────────────────────────────
    # 라우터 등록
    # ─────────────────────────────────────────────────────────────────────
    # Web (템플릿/세션)
    app.include_router(web_router)

    # API (JSON, /api/v1/*)
    app.include_router(auth_router, prefix="", tags=["auth"])
    app.include_router(nexus_router, prefix="", tags=["nexus"])
    app.include_router(pylon_router, prefix="", tags=["pylon"])

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("UVICORN_HOST", "127.0.0.1"),
        port=int(os.getenv("UVICORN_PORT", "1993")),
        reload=False,
        # reload=os.getenv("UVICORN_RELOAD", "true").lower() == "true",
    )
    uvicorn.run(app, host="127.0.0.1", port=1993)



