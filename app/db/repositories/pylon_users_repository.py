from sqlalchemy.orm import Session
from app.db.models.pylon_users import PylonUsers

class PylonUsersRepository:
    def get_pylon_user(self, db: Session, id: int) -> PylonUsers | None:
        """ID로 pylon_user 조회"""
        return db.query(PylonUsers).filter(PylonUsers.id == id).first()

    def get_pylon_users_by_pylon(self, db: Session, pylon_id: int) -> list[PylonUsers]:
        """특정 pylon의 모든 사용자 조회"""
        return db.query(PylonUsers).filter(PylonUsers.pylon_id == pylon_id).all()

    def get_pylon_users_by_user(self, db: Session, user_id: str) -> list[PylonUsers]:
        """특정 사용자가 속한 모든 pylon 조회"""
        return db.query(PylonUsers).filter(PylonUsers.user_id == user_id).all()

    def get_pylon_user_by_pylon_and_user(self, db: Session, pylon_id: int, user_id: str) -> PylonUsers | None:
        """특정 pylon과 user의 관계 조회"""
        return (
            db.query(PylonUsers)
            .filter(PylonUsers.pylon_id == pylon_id, PylonUsers.user_id == user_id)
            .first()
        )

    def create(self,
               db: Session,
               pylon_id: int,
               user_id: str,
               user_role: str,
               user_image_url: str,
               pylon_role: str = "owner") -> PylonUsers:
        """새 pylon_user 생성"""
        pylon_user = PylonUsers(
            pylon_id=pylon_id,
            user_id=user_id,
            user_role=user_role,
            pylon_role=pylon_role,
            user_image_url=user_image_url,
        )
        db.add(pylon_user)
        db.commit()
        db.refresh(pylon_user)
        return pylon_user

    def update(self,
               db: Session,
               id: int,
               user_role: str | None = None,
               pylon_role: str | None = None,
               user_image_url: str | None = None) -> PylonUsers | None:
        """pylon_user 업데이트"""
        pylon_user = self.get_pylon_user(db, id)
        if not pylon_user:
            return None

        if user_role is not None:
            pylon_user.user_role = user_role
        if pylon_role is not None:
            pylon_user.pylon_role = pylon_role
        if user_image_url is not None:
            pylon_user.user_image_url = user_image_url

        db.commit()
        db.refresh(pylon_user)
        return pylon_user

    def delete(self, db: Session, id: int) -> bool:
        """pylon_user 삭제"""
        pylon_user = self.get_pylon_user(db, id)
        if not pylon_user:
            return False

        db.delete(pylon_user)
        db.commit()
        return True

    def delete_by_pylon_and_user(self, db: Session, pylon_id: int, user_id: str) -> bool:
        """특정 pylon에서 사용자 제거"""
        pylon_user = self.get_pylon_user_by_pylon_and_user(db, pylon_id, user_id)
        if not pylon_user:
            return False

        db.delete(pylon_user)
        db.commit()
        return True
