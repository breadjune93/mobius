import sys
import os
import json
import datetime
import traceback

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session

from ai.system_prompt import FULLSTACK_DEVELOPER
from ai.tools.claude_agent import stream_claude

from app.core.deps import get_db, get_current_subject
from app.api.v1.schemas.pylon_schema import *
from app.api.v1.schemas.pylon_users_schema import *
from app.api.v1.schemas.pylon_agents_schema import *
from app.api.v1.services.pylon_service import PylonService
from app.api.v1.services.pylon_users_service import PylonUsersService
from app.api.v1.services.pylon_agents_service import PylonAgentsService
from app.db.repositories.pylon_users_repository import PylonUsersRepository
from app.db.repositories.pylon_agents_repository import PylonAgentsRepository
from app.db.repositories.agent_repository import AgentRepository
from app.db.repositories.chat_repository import ChatRepository
from typing import AsyncGenerator


router = APIRouter(prefix="/api/v1/pylon", tags=["pylon"])

# Service 초기화
pylon_service = PylonService(AgentRepository(),ChatRepository())
user_service = PylonUsersService(PylonUsersRepository())
agent_service = PylonAgentsService(PylonAgentsRepository())

# ============================================
# Agent Endpoints
# ============================================
@router.get("/agents", response_model=GetAgentsResponse)
def get_agents(
    is_active: bool = None,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """에이전트 목록 조회"""
    agents = pylon_service.get_agents(db, is_active)
    return {"agents": agents}


@router.get("/agent/{agent_id}", response_model=GetAgentResponse)
def get_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """에이전트 조회"""
    agent = pylon_service.get_agent(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"agent": agent}

# ============================================
# pylon user Endpoints
# ============================================
@router.get("/{pylon_id}/users", response_model=GetPylonUsersResponse)
def get_pylon_users(pylon_id: int, db: Session = Depends(get_db)):
    """pylon_user 조회"""
    pylon_users = user_service.get_users(db, pylon_id)
    if not pylon_users:
        raise HTTPException(status_code=404, detail="PylonUser not found")
    return {"pylon_users": pylon_users}

@router.get("/{pylon_id}/user/{pylon_user_id}", response_model=GetPylonUserResponse)
def get_pylon_user(pylon_user_id: int, db: Session = Depends(get_db)):
    """pylon_user 조회"""
    pylon_user = user_service.get_user(db, pylon_user_id)
    if not pylon_user:
        raise HTTPException(status_code=404, detail="PylonUser not found")
    return {"pylon_user": pylon_user}


# ============================================
# pylon agents Endpoints
# ============================================
@router.get("/{pylon_id}/agents", response_model=GetPylonUserResponse)
def get_pylon_user(pylon_id: int, db: Session = Depends(get_db)):
    """pylon_user 조회"""
    pylon_agents = agent_service.get_agents(db, pylon_id)
    if not pylon_agents:
        raise HTTPException(status_code=404, detail="PylonUser not found")
    return {"pylon_agents": pylon_agents}

@router.get("/{pylon_id}/agent/{agent_id}", response_model=GetPylonUserResponse)
def get_pylon_user(pylon_agent_id: int, db: Session = Depends(get_db)):
    """pylon_user 조회"""
    pylon_agent = agent_service.get_agent(db, pylon_agent_id)
    if not pylon_agent:
        raise HTTPException(status_code=404, detail="PylonUser not found")
    return {"pylon_agent": pylon_agent}

# ============================================
# Chat Endpoints
# ============================================
@router.get("/chats/{pylon_id}", response_model=GetChatsResponse)
def get_chats(
    pylon_id: int,
    limit: int = 100,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """pylon_agent의 채팅 내역 조회"""
    # Note: 이제 session_id 대신 pylon_agent_id 사용
    # chats 테이블 구조가 변경되면 여기도 수정 필요
    chats = pylon_service.get_chats(db, pylon_id, limit)
    return {"chats": chats}


# ============================================
# Streaming Chat Endpoint
# ============================================
@router.post("/stream/claude")
async def chat_stream(request: Request, payload: ChatRequest):
    print("chat_stream 호출")

    async def event_generator() -> AsyncGenerator[str, None]:
        try:
            async for chunk in stream_claude(
                system_prompt=FULLSTACK_DEVELOPER,
                prompt=payload.message
            ):
                if await request.is_disconnected():
                    break

                yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
        except Exception as e:
            print(f"스트림 에러: {e}")
            error_msg = f"{type(e).__name__}: {str(e)}"
            traceback_str = traceback.format_exc()
            error_data = json.dumps({"error": error_msg, "traceback": traceback_str, "done": True}, ensure_ascii=False)
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream; charset=utf-8"
        }
    )