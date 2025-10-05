from sqlalchemy.orm import Session
from app.db.models.workspaces import Workspaces

class WorkspaceRepository:
    def get_workspaces(self, db: Session, user_id: str) -> list[type[Workspaces]]:
        return (
            db.query(Workspaces)
            .filter(Workspaces.owner == user_id)
            .all()
        )

    def get_workspace(self, db: Session, workspace_id: int) -> Workspaces | None:
        return db.query(Workspaces).filter(Workspaces.id == workspace_id).first()

    def create(self,
               db: Session,
               title: str,
               description: str,
               user_id: str,
               goal: str,
               image_url: str = None) -> Workspaces:
        ws = Workspaces(
            title=title,
            description=description,
            goal=goal,
            owner=user_id,
            user_count=1,
            agent_count=0,
            image_url=image_url,
        )
        db.add(ws)
        db.commit()
        db.refresh(ws)
        return ws

    def update(self,
               db: Session,
               workspace_id: int,
               title: str | None = None,
               description: str | None = None,
               goal: str | None = None,
               owner: str | None = None) -> Workspaces | None:
        ws = self.get_workspace(workspace_id)
        if not ws:
            return None

        if title is not None:
            ws.title = title
        if description is not None:
            ws.description = description
        if goal is not None:
            ws.goal = goal
        if owner is not None:
            ws.owner = owner

        db.commit()
        db.refresh(ws)
        return ws

    def delete(self, db: Session, workspace_id: int) -> bool:
        ws = self.get_workspace(workspace_id)
        if not ws:
            return False

        db.delete(ws)
        db.commit()
        return True
