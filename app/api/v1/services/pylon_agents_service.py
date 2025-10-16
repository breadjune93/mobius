from sqlalchemy.orm import Session
from app.db.repositories.pylon_agents_repository import PylonAgentsRepository
from app.db.models.pylon_agents import PylonAgents
from typing import List, Optional

class PylonAgentsService:
    def __init__(self, pylon_agents_repository: PylonAgentsRepository):
        self.pylon_agents_repository = pylon_agents_repository

    def get_pylon_agent(self, db: Session, id: int) -> PylonAgents | None:
        """pylon_agent 조회"""
        return self.pylon_agents_repository.get_pylon_agent(db, id)

    def get_pylon_agents_by_pylon(self, db: Session, pylon_id: int) -> List[PylonAgents]:
        """특정 pylon의 모든 에이전트 조회"""
        return self.pylon_agents_repository.get_pylon_agents_by_pylon(db, pylon_id)

    def get_pylon_agents_by_agent(self, db: Session, agent_id: str) -> List[PylonAgents]:
        """특정 에이전트가 속한 모든 pylon 조회"""
        return self.pylon_agents_repository.get_pylon_agents_by_agent(db, agent_id)

    def get_pylon_agent_by_pylon_and_agent(self, db: Session, pylon_id: int, agent_id: str) -> PylonAgents | None:
        """특정 pylon과 agent의 관계 조회"""
        return self.pylon_agents_repository.get_pylon_agent_by_pylon_and_agent(db, pylon_id, agent_id)

    def get_active_pylon_agent(self, db: Session, pylon_id: int, agent_id: str) -> PylonAgents | None:
        """특정 pylon과 agent의 활성 세션이 있는 관계 조회"""
        return self.pylon_agents_repository.get_active_pylon_agent(db, pylon_id, agent_id)

    def create_pylon_agent(self,
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
        return self.pylon_agents_repository.create(
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

    def update_pylon_agent(self,
                           db: Session,
                           id: int,
                           **kwargs) -> PylonAgents | None:
        """pylon_agent 업데이트"""
        return self.pylon_agents_repository.update(db, id, **kwargs)

    def delete_pylon_agent(self, db: Session, id: int) -> bool:
        """pylon_agent 삭제"""
        return self.pylon_agents_repository.delete(db, id)

    def delete_pylon_agent_by_pylon_and_agent(self, db: Session, pylon_id: int, agent_id: str) -> bool:
        """특정 pylon에서 에이전트 제거"""
        return self.pylon_agents_repository.delete_by_pylon_and_agent(db, pylon_id, agent_id)

    def update_session_state(self, db: Session, id: int, session_state: str, session_id: str | None = None) -> PylonAgents | None:
        """세션 상태 업데이트"""
        return self.pylon_agents_repository.update_session_state(db, id, session_state, session_id)

    def update_pylon_agent_stats(self,
                                  db: Session,
                                  id: int,
                                  tokens_used: int = 0,
                                  tool_calls: int = 0,
                                  turns_completed: int = 0,
                                  response_time: int | None = None) -> PylonAgents | None:
        """통계 업데이트"""
        return self.pylon_agents_repository.update_stats(
            db, id, tokens_used, tool_calls, turns_completed, response_time
        )

    def create_checkpoint(self, db: Session, id: int) -> PylonAgents | None:
        """체크포인트 생성"""
        return self.pylon_agents_repository.create_checkpoint(db, id)
