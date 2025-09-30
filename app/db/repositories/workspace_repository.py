from typing import Any

from sqlalchemy.orm import Session
from app.db.models.workspaces import Workspaces

class WorkspaceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_workspaces(self, user_id: str) -> list[type[Workspaces]]:
        return (
            self.db.query(Workspaces)
            .filter(Workspaces.owner == user_id)
            .all()
        )

    def get_workspace(self, workspace_id: int) -> Workspaces | None:
        return self.db.query(Workspaces).filter(Workspaces.id == workspace_id).first()

    def create(self,
               title: str,
               description: str,
               user_id: str,
               goal: str) -> Workspaces:
        ws = Workspaces(
            title=title,
            description=description,
            goal=goal,
            owner=user_id,
            user_count=1,
            agent_count=0,
        )
        self.db.add(ws)
        self.db.commit()
        self.db.refresh(ws)
        return ws

    def update(self,
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

        self.db.commit()
        self.db.refresh(ws)
        return ws

    def delete(self, workspace_id: int) -> bool:
        ws = self.get_workspace(workspace_id)
        if not ws:
            return False

        self.db.delete(ws)
        self.db.commit()
        return True
