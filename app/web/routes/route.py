from fastapi import APIRouter, Request, status
from fastapi.responses import FileResponse, RedirectResponse

import os
router = APIRouter()
current_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
views_dir = os.path.join(current_dir, "templates")

from app.core.security import delete_token


@router.get("/signup")
def signup():
    return FileResponse(os.path.join(views_dir, "signup.html"))

@router.get("/login")
def login():
    return FileResponse(os.path.join(views_dir, "login.html"))

@router.get("/forgot-password")
def forgot_password():
    return FileResponse(os.path.join(views_dir, "forgot-password.html"))

@router.get("/")
def root():
    return RedirectResponse(url="/nexus", status_code=status.HTTP_302_FOUND)

@router.get("/nexus")
def nexus():
    return FileResponse(os.path.join(views_dir, "nexus.html"))

@router.get("/workspace/{room_id}")
def workspace():
    return FileResponse(os.path.join(views_dir, "mission.html"))

@router.post("/logout")
def logout(request: Request):
    delete_token(request)
    return {"message": "로그아웃되었습니다"}