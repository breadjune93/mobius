from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_subject
from app.api.v1.schemas.pylon_users_schema import *
from app.api.v1.services.pylon_users_service import PylonUsersService
from app.db.repositories.pylon_users_repository import PylonUsersRepository

router = APIRouter(prefix="/api/v1/pylon/user", tags=["pylon-user"])

# Service 초기화
service = PylonUsersService(PylonUsersRepository())


# ============================================
# PylonUsers Endpoints
# ============================================
@router.get("/{id}", response_model=GetPylonUserResponse)
def get_pylon_user(
    id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """pylon_user 조회"""
    pylon_user = service.get_pylon_user(db, id)
    if not pylon_user:
        raise HTTPException(status_code=404, detail="PylonUser not found")
    return {"pylon_user": pylon_user}


@router.get("/pylon/{pylon_id}", response_model=GetPylonUsersResponse)
def get_pylon_users_by_pylon(
    pylon_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """특정 pylon의 모든 사용자 조회"""
    pylon_users = service.get_pylon_users_by_pylon(db, pylon_id)
    return {"pylon_users": pylon_users}


@router.get("/user/{user_id_param}", response_model=GetPylonUsersResponse)
def get_pylon_users_by_user(
    user_id_param: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """특정 사용자가 속한 모든 pylon 조회"""
    pylon_users = service.get_pylon_users_by_user(db, user_id_param)
    return {"pylon_users": pylon_users}


@router.post("/", response_model=GetPylonUserResponse)
def create_pylon_user(
    payload: CreatePylonUserRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """새 pylon_user 생성"""
    try:
        pylon_user = service.create_pylon_user(
            db=db,
            pylon_id=payload.pylon_id,
            user_id=payload.user_id,
            user_role=payload.user_role,
            user_image_url=payload.user_image_url,
            pylon_role=payload.pylon_role
        )
        return {"pylon_user": pylon_user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create pylon_user: {str(e)}")


@router.patch("/{id}", response_model=GetPylonUserResponse)
def update_pylon_user(
    id: int,
    payload: UpdatePylonUserRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """pylon_user 업데이트"""
    pylon_user = service.update_pylon_user(
        db=db,
        id=id,
        user_role=payload.user_role,
        pylon_role=payload.pylon_role,
        user_image_url=payload.user_image_url
    )
    if not pylon_user:
        raise HTTPException(status_code=404, detail="PylonUser not found")
    return {"pylon_user": pylon_user}


@router.delete("/{id}")
def delete_pylon_user(
    id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """pylon_user 삭제"""
    success = service.delete_pylon_user(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="PylonUser not found")
    return {"message": "PylonUser deleted successfully"}


@router.delete("/pylon/{pylon_id}/user/{user_id_param}")
def delete_pylon_user_by_pylon_and_user(
    pylon_id: int,
    user_id_param: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_subject)
):
    """특정 pylon에서 사용자 제거"""
    success = service.delete_pylon_user_by_pylon_and_user(db, pylon_id, user_id_param)
    if not success:
        raise HTTPException(status_code=404, detail="PylonUser relationship not found")
    return {"message": "User removed from pylon successfully"}
