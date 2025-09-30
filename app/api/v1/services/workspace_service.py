from app.db.repositories.workspace_repository import WorkspaceRepository
from app.db.models.workspaces import Workspaces

class WorkspaceService:
    def __init__(self, workspace_repository: WorkspaceRepository):
        self.workspace_repository = workspace_repository

    def get_workspaces(self, user_id: str) -> list[type[Workspaces]]:
        return self.workspace_repository.get_workspaces(user_id)

    def get_workspace(self, workspace_id: int) -> Workspaces | None:
        return self.workspace_repository.get_workspace(workspace_id)

    def create_workspace(self,
                         title: str,
                         description: str,
                         user_id: str,
                         goal: str = "NORMAL") -> Workspaces:
        return self.workspace_repository.create(
            title=title,
            description=description,
            user_id=user_id,
            goal=goal,
        )

    def update_workspace(self,
                         workspace_id: int,
                         title: str | None = None,
                         description: str | None = None,
                         goal: str | None = None,
                         owner: str | None = None) -> Workspaces | None:
        return self.workspace_repository.update(
            workspace_id=workspace_id,
            title=title,
            description=description,
            goal=goal,
            owner=owner,
        )

    def delete_workspace(self, workspace_id: int) -> bool:
        return self.workspace_repository.delete(workspace_id)
