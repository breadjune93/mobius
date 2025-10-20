from sqlalchemy.orm import Session
from app.db.repositories.pylon_users_repository import PylonUsersRepository
from app.db.models.pylon_users import PylonUsers

class PylonUsersService:
    def __init__(self, pylon_users_repository: PylonUsersRepository):
        self.pylon_users_repository = pylon_users_repository

    def get_users(self, db: Session, pylon_id: int) -> list[type[PylonUsers]]:
        """특정 pylon의 모든 사용자 조회"""
        return self.pylon_users_repository.get_user_by_pylon(db, pylon_id)

    def get_user(self, db: Session, pylon_user_id: int) -> PylonUsers | None:
        """특정 pylon과 user의 관계 조회"""
        return self.pylon_users_repository.get_user_by_id(db, pylon_user_id)

    def create_user(self,
                          db: Session,
                          pylon_id: int,
                          user_id: str,
                          user_role: str,
                          user_image_url: str,
                          pylon_role: str = "owner") -> PylonUsers:
        """새 pylon_user 생성"""
        return self.pylon_users_repository.create_user(
            db=db,
            pylon_id=pylon_id,
            user_id=user_id,
            user_role=user_role,
            user_image_url=user_image_url,
            pylon_role=pylon_role
        )

    def update_user(self,
                          db: Session,
                          pylon_user_id: int,
                          user_role: str | None = None,
                          pylon_role: str | None = None,
                          user_image_url: str | None = None) -> PylonUsers | None:
        """pylon_user 업데이트"""
        return self.pylon_users_repository.update_user(
            db=db,
            pylon_user_id=pylon_user_id,
            user_role=user_role,
            pylon_role=pylon_role,
            user_image_url=user_image_url
        )

    def delete_user(self, db: Session, pylon_user_id: int) -> bool:
        """pylon_user 삭제"""
        return self.pylon_users_repository.delete_user(db, pylon_user_id)