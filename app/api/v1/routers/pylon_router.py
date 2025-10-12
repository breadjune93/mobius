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
from app.api.v1.services.pylon_service import PylonService
from app.db.repositories.agent_repository import AgentRepository
from app.db.repositories.session_repository import SessionRepository
from app.db.repositories.chat_repository import ChatRepository
from typing import AsyncGenerator


router = APIRouter(prefix="/api/v1/pylon", tags=["pylon"])

# Service 초기화
service = PylonService(
    AgentRepository(),
    SessionRepository(),
    ChatRepository()
)

# ============================================
# Session Endpoints
# ============================================
@router.get("/session/{session_id}", response_model=GetSessionResponse)
def get_session(
    session_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """세션 조회"""
    session = service.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session": session}


@router.post("/session", response_model=GetSessionResponse)
def create_session(
    payload: CreateSessionRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """새 세션 생성"""
    try:
        session, agent = service.create_session_with_agent(
            db=db,
            pylon_id=payload.pylon_id,
            agent_id=payload.agent_id,
            working_directory=payload.working_directory
        )
        return {"session": session}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


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
    agents = service.get_agents(db, is_active)
    return {"agents": agents}


@router.get("/agent/{agent_id}", response_model=GetAgentResponse)
def get_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """에이전트 조회"""
    agent = service.get_agent(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"agent": agent}


# ============================================
# Chat Endpoints
# ============================================
@router.get("/chats/{session_id}", response_model=GetChatsResponse)
def get_chats(
    session_id: str,
    limit: int = 100,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """세션의 채팅 내역 조회"""
    # 세션 존재 확인
    session = service.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    chats = service.get_chats(db, session_id, limit)
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