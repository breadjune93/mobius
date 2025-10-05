from sqlalchemy.orm import Session
from app.db.models.pylons import Pylons

class PylonRepository:
    def get_pylons(self, db: Session, user_id: str) -> list[type[Pylons]]:
        return (
            db.query(Pylons)
            .filter(Pylons.owner == user_id)
            .all()
        )

    def get_pylon(self, db: Session, pylon_id: int) -> Pylons | None:
        return db.query(Pylons).filter(Pylons.id == pylon_id).first()

    def create(self,
               db: Session,
               title: str,
               description: str,
               user_id: str,
               goal: str,
               image_url: str = None) -> Pylons:
        pylon = Pylons(
            title=title,
            description=description,
            goal=goal,
            owner=user_id,
            user_count=1,
            agent_count=0,
            image_url=image_url,
        )
        db.add(pylon)
        db.commit()
        db.refresh(pylon)
        return pylon

    def update(self,
               db: Session,
               pylon_id: int,
               title: str | None = None,
               description: str | None = None,
               goal: str | None = None,
               owner: str | None = None) -> Pylons | None:
        pylon = self.get_pylon(db, pylon_id)
        if not pylon:
            return None

        if title is not None:
            pylon.title = title
        if description is not None:
            pylon.description = description
        if goal is not None:
            pylon.goal = goal
        if owner is not None:
            pylon.owner = owner

        db.commit()
        db.refresh(pylon)
        return pylon

    def delete(self, db: Session, pylon_id: int) -> bool:
        pylon = self.get_pylon(db, pylon_id)
        if not pylon:
            return False

        db.delete(pylon)
        db.commit()
        return True
