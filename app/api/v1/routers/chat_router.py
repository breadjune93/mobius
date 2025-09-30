import sys
import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from agent.tool_agents import ToolAgents
import json
import datetime

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

# TestAgent 인스턴스를 한번만 생성
tool_agents = ToolAgents()

class ChatRequest(BaseModel):
    message: str

class RoomCreateRequest(BaseModel):
    title: str
    description: Optional[str] = ""
    type: str = "general"  # general, development, design, deployment
    privacy: str = "public"  # public, private

class RoomResponse(BaseModel):
    id: int
    title: str
    description: str
    type: str
    privacy: str
    participants: int
    lastActivity: str
    status: str
    createdAt: str
    createdBy: str

# 임시 데이터 저장소 (실제로는 데이터베이스 사용)
rooms_db = [
    {
        "id": 1,
        "title": "프로젝트 개발 상담",
        "description": "React와 Node.js 프로젝트 관련 질문",
        "type": "development",
        "privacy": "public",
        "participants": 5,
        "lastActivity": "2분 전",
        "status": "active",
        "createdAt": "2024-09-20T10:00:00",
        "createdBy": "admin"
    },
    {
        "id": 2,
        "title": "UI/UX 디자인 피드백",
        "description": "웹사이트 디자인 개선 아이디어 논의",
        "type": "design",
        "privacy": "public",
        "participants": 3,
        "lastActivity": "15분 전",
        "status": "active",
        "createdAt": "2024-09-20T09:45:00",
        "createdBy": "designer1"
    },
    {
        "id": 3,
        "title": "배포 및 서버 관리",
        "description": "AWS 배포 관련 도움이 필요합니다",
        "type": "deployment",
        "privacy": "public",
        "participants": 2,
        "lastActivity": "1시간 전",
        "status": "inactive",
        "createdAt": "2024-09-20T08:30:00",
        "createdBy": "devops1"
    }
]

@router.get("/rooms")
def get_rooms() -> List[RoomResponse]:
    """채팅방 목록 조회"""
    return [RoomResponse(**room) for room in rooms_db]

@router.post("/rooms")
def create_room(room_data: RoomCreateRequest) -> RoomResponse:
    """새 채팅방 생성"""
    # 새 room ID 생성
    new_id = max([room["id"] for room in rooms_db], default=0) + 1

    # 새 채팅방 데이터 생성
    new_room = {
        "id": new_id,
        "title": room_data.title,
        "description": room_data.description,
        "type": room_data.type,
        "privacy": room_data.privacy,
        "participants": 1,  # 생성자가 첫 참여자
        "lastActivity": "방금 전",
        "status": "active",
        "createdAt": datetime.datetime.now().isoformat(),
        "createdBy": "current_user"  # 실제로는 인증된 사용자 정보 사용
    }

    # 임시 DB에 추가
    rooms_db.append(new_room)

    return RoomResponse(**new_room)

@router.get("/rooms/{room_id}")
def get_room(room_id: int) -> RoomResponse:
    """특정 채팅방 정보 조회"""
    room = next((room for room in rooms_db if room["id"] == room_id), None)
    if not room:
        raise HTTPException(status_code=404, detail="채팅방을 찾을 수 없습니다")

    return RoomResponse(**room)

@router.delete("/rooms/{room_id}")
def delete_room(room_id: int):
    """채팅방 삭제"""
    global rooms_db
    room_index = next((i for i, room in enumerate(rooms_db) if room["id"] == room_id), None)
    if room_index is None:
        raise HTTPException(status_code=404, detail="채팅방을 찾을 수 없습니다")

    # 권한 체크 (실제로는 방 생성자나 관리자만 삭제 가능)
    # if rooms_db[room_index]["createdBy"] != current_user:
    #     raise HTTPException(status_code=403, detail="권한이 없습니다")

    rooms_db.pop(room_index)
    return {"message": "채팅방이 삭제되었습니다"}

@router.post("/rooms/{room_id}/join")
def join_room(room_id: int):
    """채팅방 참여"""
    room = next((room for room in rooms_db if room["id"] == room_id), None)
    if not room:
        raise HTTPException(status_code=404, detail="채팅방을 찾을 수 없습니다")

    # 참여자 수 증가 (실제로는 중복 참여 체크 필요)
    room["participants"] += 1
    room["lastActivity"] = "방금 전"
    room["status"] = "active"

    return {"message": "채팅방에 참여했습니다", "room_id": room_id}



@router.post("/chat")
async def chat_stream(request: ChatRequest):
    async def generate():
        try:
            async for chunk in tool_agents.chat(request.message):
                yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"

        except Exception as e:
            error_data = json.dumps({"error": str(e), "done": True}, ensure_ascii=False)
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )