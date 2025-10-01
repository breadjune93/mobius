from sqlalchemy.orm import Session
from app.db.repositories.workspace_repository import WorkspaceRepository
from app.db.models.workspaces import Workspaces

class WorkspaceService:
    def __init__(self, workspace_repository: WorkspaceRepository):
        self.workspace_repository = workspace_repository

    def get_workspaces(self, db: Session, user_id: str):
        return self.workspace_repository.get_workspaces(db, user_id)

    def get_workspace(self, db: Session, workspace_id: int) -> Workspaces | None:
        return self.workspace_repository.get_workspace(db, workspace_id)

    def create_workspace(self,
                         db: Session,
                         title: str,
                         description: str,
                         user_id: str,
                         goal: str = "NORMAL"):
        workspace = self.workspace_repository.create(
            db=db,
            title=title,
            description=description,
            user_id=user_id,
            goal=goal,
        )

        return workspace

        # return {
        #     "id": workspace.id,
        #     "title": workspace.title,
        #     "description": workspace.description,
        #     "goal": workspace.goal,
        #     "owner": workspace.owner,
        #     "user_count": workspace.user_count,
        #     "agent_count": workspace.agent_count,
        #     "created_at": workspace.created_at
        # }

    def update_workspace(self,
                         db: Session,
                         workspace_id: int,
                         title: str | None = None,
                         description: str | None = None,
                         goal: str | None = None,
                         owner: str | None = None) -> Workspaces | None:
        return self.workspace_repository.update(
            db=db,
            workspace_id=workspace_id,
            title=title,
            description=description,
            goal=goal,
            owner=owner,
        )

    def delete_workspace(self, db: Session, workspace_id: int) -> bool:
        return self.workspace_repository.delete(db, workspace_id)
