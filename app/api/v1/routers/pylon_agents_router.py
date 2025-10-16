from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_subject
from app.api.v1.schemas.pylon_agents_schema import *
from app.api.v1.services.pylon_agents_service import PylonAgentsService
from app.db.repositories.pylon_agents_repository import PylonAgentsRepository

router = APIRouter(prefix="/api/v1/pylon-agents", tags=["pylon-agents"])

# Service 초기화
service = PylonAgentsService(PylonAgentsRepository())


# ============================================
# PylonAgents Endpoints
# ============================================
@router.get("/{id}", response_model=GetPylonAgentResponse)
def get_pylon_agent(
    id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """pylon_agent 조회"""
    pylon_agent = service.get_pylon_agent(db, id)
    if not pylon_agent:
        raise HTTPException(status_code=404, detail="PylonAgent not found")
    return {"pylon_agent": pylon_agent}


@router.get("/pylon/{pylon_id}", response_model=GetPylonAgentsResponse)
def get_pylon_agents_by_pylon(
    pylon_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """특정 pylon의 모든 에이전트 조회"""
    pylon_agents = service.get_pylon_agents_by_pylon(db, pylon_id)
    return {"pylon_agents": pylon_agents}


@router.get("/agent/{agent_id}", response_model=GetPylonAgentsResponse)
def get_pylon_agents_by_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """특정 에이전트가 속한 모든 pylon 조회"""
    pylon_agents = service.get_pylon_agents_by_agent(db, agent_id)
    return {"pylon_agents": pylon_agents}


@router.get("/pylon/{pylon_id}/agent/{agent_id}", response_model=GetPylonAgentResponse)
def get_pylon_agent_by_pylon_and_agent(
    pylon_id: int,
    agent_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """특정 pylon과 agent의 관계 조회"""
    pylon_agent = service.get_pylon_agent_by_pylon_and_agent(db, pylon_id, agent_id)
    if not pylon_agent:
        raise HTTPException(status_code=404, detail="PylonAgent relationship not found")
    return {"pylon_agent": pylon_agent}


@router.post("/", response_model=GetPylonAgentResponse)
def create_pylon_agent(
    payload: CreatePylonAgentRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """새 pylon_agent 생성"""
    try:
        pylon_agent = service.create_pylon_agent(
            db=db,
            pylon_id=payload.pylon_id,
            agent_id=payload.agent_id,
            agent_image_url=payload.agent_image_url,
            working_directory=payload.working_directory,
            session_id=payload.session_id,
            session_state=payload.session_state,
            claude_md_content=payload.claude_md_content,
            mcp_servers=payload.mcp_servers,
            subagents_enabled=payload.subagents_enabled,
            active_subagents=payload.active_subagents,
            memory_enabled=payload.memory_enabled,
            memory_directory=payload.memory_directory,
            allowed_tools=payload.allowed_tools,
            disallowed_tools=payload.disallowed_tools
        )
        return {"pylon_agent": pylon_agent}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create pylon_agent: {str(e)}")


@router.patch("/{id}", response_model=GetPylonAgentResponse)
def update_pylon_agent(
    id: int,
    payload: UpdatePylonAgentRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """pylon_agent 업데이트"""
    update_data = payload.dict(exclude_unset=True)
    pylon_agent = service.update_pylon_agent(db, id, **update_data)
    if not pylon_agent:
        raise HTTPException(status_code=404, detail="PylonAgent not found")
    return {"pylon_agent": pylon_agent}


@router.patch("/{id}/stats", response_model=GetPylonAgentResponse)
def update_pylon_agent_stats(
    id: int,
    payload: UpdatePylonAgentStatsRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """pylon_agent 통계 업데이트"""
    pylon_agent = service.update_pylon_agent_stats(
        db=db,
        id=id,
        tokens_used=payload.tokens_used,
        tool_calls=payload.tool_calls,
        turns_completed=payload.turns_completed,
        response_time=payload.response_time
    )
    if not pylon_agent:
        raise HTTPException(status_code=404, detail="PylonAgent not found")
    return {"pylon_agent": pylon_agent}


@router.post("/{id}/checkpoint", response_model=GetPylonAgentResponse)
def create_checkpoint(
    id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """체크포인트 생성"""
    pylon_agent = service.create_checkpoint(db, id)
    if not pylon_agent:
        raise HTTPException(status_code=404, detail="PylonAgent not found")
    return {"pylon_agent": pylon_agent}


@router.delete("/{id}")
def delete_pylon_agent(
    id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """pylon_agent 삭제"""
    success = service.delete_pylon_agent(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="PylonAgent not found")
    return {"message": "PylonAgent deleted successfully"}


@router.delete("/pylon/{pylon_id}/agent/{agent_id}")
def delete_pylon_agent_by_pylon_and_agent(
    pylon_id: int,
    agent_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """특정 pylon에서 에이전트 제거"""
    success = service.delete_pylon_agent_by_pylon_and_agent(db, pylon_id, agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="PylonAgent relationship not found")
    return {"message": "Agent removed from pylon successfully"}
