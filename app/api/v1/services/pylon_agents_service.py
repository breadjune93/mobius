from sqlalchemy.orm import Session
from app.db.repositories.pylon_agents_repository import PylonAgentsRepository
from app.db.models.pylon_agents import PylonAgents

class PylonAgentsService:
    def __init__(self, pylon_agents_repository: PylonAgentsRepository):
        self.pylon_agents_repository = pylon_agents_repository

    def get_agents(self, db: Session, pylon_id: int) -> list[type[PylonAgents]]:
        """pylon_agents 조회"""
        return self.pylon_agents_repository.get_agent_by_pylon(db, pylon_id)

    def get_agent(self, db: Session, pylon_agent_id: int) -> PylonAgents | None:
        """pylon_agent 조회"""
        return self.pylon_agents_repository.get_agent_by_id(db, pylon_agent_id)

    def create_agent(self,
                           db: Session,
                           pylon_id: int,
                           agent_id: str,
                           agent_image_url: str,
                           working_directory: str,
                           session_id: str | None = None,
                           session_state: str = "active",
                           claude_md_content: str | None = None,
                           mcp_servers: dict | None = None,
                           subagents_enabled: bool = False,
                           active_subagents: dict | None = None,
                           memory_enabled: bool = False,
                           memory_directory: str | None = None,
                           allowed_tools: dict | None = None,
                           disallowed_tools: dict | None = None) -> PylonAgents:
        """새 pylon_agent 생성"""
        return self.pylon_agents_repository.create_agent(
            db=db,
            pylon_id=pylon_id,
            agent_id=agent_id,
            agent_image_url=agent_image_url,
            working_directory=working_directory,
            session_id=session_id,
            session_state=session_state,
            claude_md_content=claude_md_content,
            mcp_servers=mcp_servers,
            subagents_enabled=subagents_enabled,
            active_subagents=active_subagents,
            memory_enabled=memory_enabled,
            memory_directory=memory_directory,
            allowed_tools=allowed_tools,
            disallowed_tools=disallowed_tools
        )

    def update_agent(self,
                           db: Session,
                           pylon_agent_id: int,
                           **kwargs) -> PylonAgents | None:
        """pylon_agent 업데이트"""
        return self.pylon_agents_repository.update_agent(db, pylon_agent_id, **kwargs)

    def delete_agent(self, db: Session, pylon_agent_id: int) -> bool:
        """pylon_agent 삭제"""
        return self.pylon_agents_repository.delete_agent(db, pylon_agent_id)