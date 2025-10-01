from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.api.v1.schemas.workspace_schema import *
from app.api.v1.services.workspace_service import WorkspaceService
from app.db.repositories.workspace_repository import WorkspaceRepository
from app.db.models.workspaces import Workspaces

router = APIRouter(prefix="/api/v1/nexus", tags=["nexus"])
service = WorkspaceService(WorkspaceRepository())

# 워크스페이스 리스트 조회
@router.get("/workspaces", response_model=GetWorkspacesResponse)
def get_workspaces(payload: GetWorkspacesRequest, db: Session = Depends(get_db)):
    workspaces = service.get_workspaces(db, payload.user_id)
    return { "workspaces": workspaces }

# 워크스페이스 생성
@router.post("/workspace", response_model=GetWorkspaceResponse)
def create_workspace(payload: CreateWorkspace, db: Session = Depends(get_db)):
    # owner는 추후 JWT에서 추출 가능, 현재는 payload.owner 사용
    workspace = service.create_workspace(db=db,
                                    title=payload.title,
                                    description=payload.description,
                                    user_id=payload.owner if payload.owner else "test_user",
                                    goal=payload.type.upper())
    return { "workspace": workspace }

# 워크스페이스 조회
# @router.get("/workspace/{workspace_id}", response_model=)
# def get_workspace():
#     return

# 워크스페이스 업데이트
# @router.put("/workspace", response_model=)
# def update_workspace():
#     return

# 워크스페이스 삭제
# @router.delete("/workspace", response_model=)
# def delete_workspace():
#     return

