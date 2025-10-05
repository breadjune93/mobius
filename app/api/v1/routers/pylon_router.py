from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_subject
from app.api.v1.schemas.pylon_schema import *
from app.api.v1.services.pylon_service import PylonService
from app.db.repositories.pylon_repository import PylonRepository
from app.db.models.pylons import Pylons

router = APIRouter(prefix="/api/v1/nexus", tags=["nexus"])
service = PylonService(PylonRepository())

# 파일론 리스트 조회
@router.get("/pylons", response_model=GetPylonsResponse)
def get_pylons(db: Session = Depends(get_db), user_id: str = Depends(get_current_subject)):
    pylons = service.get_pylons(db, user_id)
    return {"pylons": pylons}

# 파일런 생성
@router.post("/pylon", response_model=GetPylonResponse)
def create_pylon(payload: CreatePylon, db: Session = Depends(get_db), user_id: str = Depends(get_current_subject)):
    pylon = service.create_pylon(db=db,
                                    title=payload.title,
                                    description=payload.description,
                                    user_id=user_id,
                                    goal=payload.type.upper(),
                                    image_url=payload.image_url)
    return { "pylon": pylon }

# 파일런 조회
@router.get("/pylon/{pylon_id}", response_model=GetPylonResponse)
def get_pylon(pylon_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_subject)):
    pylon = service.get_pylon(db, pylon_id)
    if not pylon:
        raise HTTPException(status_code=404, detail="Pylon not found")
    return {"pylon": pylon}

# 파일런 업데이트
@router.put("/pylon/{pylon_id}", response_model=GetPylonResponse)
def update_pylon(pylon_id: int, payload: UpdatePylon, db: Session = Depends(get_db), user_id: str = Depends(get_current_subject)):
    pylon = service.update_pylon(
        db=db,
        pylon_id=pylon_id,
        title=payload.title,
        description=payload.description,
        goal=payload.goal
    )
    if not pylon:
        raise HTTPException(status_code=404, detail="Pylon not found")
    return {"pylon": pylon}

# 파일런 삭제
@router.delete("/pylon/{pylon_id}", response_model=ResultResponse)
def delete_pylon(pylon_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_subject)):
    result = service.delete_pylon(db, pylon_id)
    if not result:
        raise HTTPException(status_code=404, detail="Pylon not found")
    return {"is_succeed": True}

