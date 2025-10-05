from sqlalchemy.orm import Session
from app.db.repositories.pylon_repository import PylonRepository
from app.db.models.pylons import Pylons

class PylonService:
    def __init__(self, pylon_repository: PylonRepository):
        self.pylon_repository = pylon_repository

    def get_pylons(self, db: Session, user_id: str):
        return self.pylon_repository.get_pylons(db, user_id)

    def get_pylon(self, db: Session, pylon_id: int) -> Pylons | None:
        return self.pylon_repository.get_pylon(db, pylon_id)

    def create_pylon(self,
                         db: Session,
                         title: str,
                         description: str,
                         user_id: str,
                         goal: str = "NORMAL",
                         image_url: str = None):
        pylon = self.pylon_repository.create(
            db=db,
            title=title,
            description=description,
            user_id=user_id,
            goal=goal,
            image_url=image_url,
        )

        return pylon

        # return {
        #     "id": pylon.id,
        #     "title": pylon.title,
        #     "description": pylon.description,
        #     "goal": pylon.goal,
        #     "owner": pylon.owner,
        #     "user_count": pylon.user_count,
        #     "agent_count": pylon.agent_count,
        #     "created_at": pylon.created_at
        # }

    def update_pylon(self,
                         db: Session,
                         pylon_id: int,
                         title: str | None = None,
                         description: str | None = None,
                         goal: str | None = None,
                         owner: str | None = None) -> Pylons | None:
        return self.pylon_repository.update(
            db=db,
            pylon_id=pylon_id,
            title=title,
            description=description,
            goal=goal,
            owner=owner,
        )

    def delete_pylon(self, db: Session, pylon_id: int) -> bool:
        return self.pylon_repository.delete(db, pylon_id)
