from sqlalchemy.orm import Session
from app.db.models.pylon_agents import PylonAgents
from typing import Optional

class PylonAgentsRepository:
    def get_pylon_agent(self, db: Session, id: int) -> PylonAgents | None:
        """ID로 pylon_agent 조회"""
        return db.query(PylonAgents).filter(PylonAgents.id == id).first()

    def get_pylon_agents_by_pylon(self, db: Session, pylon_id: int) -> list[PylonAgents]:
        """특정 pylon의 모든 에이전트 조회"""
        return db.query(PylonAgents).filter(PylonAgents.pylon_id == pylon_id).all()

    def get_pylon_agents_by_agent(self, db: Session, agent_id: str) -> list[PylonAgents]:
        """특정 에이전트가 속한 모든 pylon 조회"""
        return db.query(PylonAgents).filter(PylonAgents.agent_id == agent_id).all()

    def get_pylon_agent_by_pylon_and_agent(self, db: Session, pylon_id: int, agent_id: str) -> PylonAgents | None:
        """특정 pylon과 agent의 관계 조회"""
        return (
            db.query(PylonAgents)
            .filter(PylonAgents.pylon_id == pylon_id, PylonAgents.agent_id == agent_id)
            .first()
        )

    def get_active_pylon_agent(self, db: Session, pylon_id: int, agent_id: str) -> PylonAgents | None:
        """특정 pylon과 agent의 활성 세션이 있는 관계 조회"""
        return (
            db.query(PylonAgents)
            .filter(
                PylonAgents.pylon_id == pylon_id,
                PylonAgents.agent_id == agent_id,
                PylonAgents.session_state == "active"
            )
            .first()
        )

    def create(self,
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
        pylon_agent = PylonAgents(
            pylon_id=pylon_id,
            agent_id=agent_id,
            agent_image_url=agent_image_url,
            session_id=session_id,
            session_state=session_state,
            working_directory=working_directory,
            claude_md_content=claude_md_content,
            mcp_servers=mcp_servers,
            subagents_enabled=subagents_enabled,
            active_subagents=active_subagents,
            memory_enabled=memory_enabled,
            memory_directory=memory_directory,
            allowed_tools=allowed_tools,
            disallowed_tools=disallowed_tools,
        )
        db.add(pylon_agent)
        db.commit()
        db.refresh(pylon_agent)
        return pylon_agent

    def update(self,
               db: Session,
               id: int,
               agent_image_url: str | None = None,
               session_id: str | None = None,
               session_state: str | None = None,
               working_directory: str | None = None,
               claude_md_content: str | None = None,
               mcp_servers: dict | None = None,
               subagents_enabled: bool | None = None,
               active_subagents: dict | None = None,
               memory_enabled: bool | None = None,
               memory_directory: str | None = None,
               allowed_tools: dict | None = None,
               disallowed_tools: dict | None = None,
               total_tokens_used: int | None = None,
               total_tool_calls: int | None = None,
               total_turns_completed: int | None = None,
               average_response_time: int | None = None) -> PylonAgents | None:
        """pylon_agent 업데이트"""
        pylon_agent = self.get_pylon_agent(db, id)
        if not pylon_agent:
            return None

        if agent_image_url is not None:
            pylon_agent.agent_image_url = agent_image_url
        if session_id is not None:
            pylon_agent.session_id = session_id
        if session_state is not None:
            pylon_agent.session_state = session_state
        if working_directory is not None:
            pylon_agent.working_directory = working_directory
        if claude_md_content is not None:
            pylon_agent.claude_md_content = claude_md_content
        if mcp_servers is not None:
            pylon_agent.mcp_servers = mcp_servers
        if subagents_enabled is not None:
            pylon_agent.subagents_enabled = subagents_enabled
        if active_subagents is not None:
            pylon_agent.active_subagents = active_subagents
        if memory_enabled is not None:
            pylon_agent.memory_enabled = memory_enabled
        if memory_directory is not None:
            pylon_agent.memory_directory = memory_directory
        if allowed_tools is not None:
            pylon_agent.allowed_tools = allowed_tools
        if disallowed_tools is not None:
            pylon_agent.disallowed_tools = disallowed_tools
        if total_tokens_used is not None:
            pylon_agent.total_tokens_used = total_tokens_used
        if total_tool_calls is not None:
            pylon_agent.total_tool_calls = total_tool_calls
        if total_turns_completed is not None:
            pylon_agent.total_turns_completed = total_turns_completed
        if average_response_time is not None:
            pylon_agent.average_response_time = average_response_time

        db.commit()
        db.refresh(pylon_agent)
        return pylon_agent

    def delete(self, db: Session, id: int) -> bool:
        """pylon_agent 삭제"""
        pylon_agent = self.get_pylon_agent(db, id)
        if not pylon_agent:
            return False

        db.delete(pylon_agent)
        db.commit()
        return True

    def delete_by_pylon_and_agent(self, db: Session, pylon_id: int, agent_id: str) -> bool:
        """특정 pylon에서 에이전트 제거"""
        pylon_agent = self.get_pylon_agent_by_pylon_and_agent(db, pylon_id, agent_id)
        if not pylon_agent:
            return False

        db.delete(pylon_agent)
        db.commit()
        return True

    def update_session_state(self, db: Session, id: int, session_state: str, session_id: str | None = None) -> PylonAgents | None:
        """세션 상태 업데이트"""
        return self.update(db, id, session_state=session_state, session_id=session_id)

    def update_stats(self,
                     db: Session,
                     id: int,
                     tokens_used: int = 0,
                     tool_calls: int = 0,
                     turns_completed: int = 0,
                     response_time: int | None = None) -> PylonAgents | None:
        """통계 업데이트"""
        pylon_agent = self.get_pylon_agent(db, id)
        if not pylon_agent:
            return None

        pylon_agent.total_tokens_used = (pylon_agent.total_tokens_used or 0) + tokens_used
        pylon_agent.total_tool_calls = (pylon_agent.total_tool_calls or 0) + tool_calls
        pylon_agent.total_turns_completed = (pylon_agent.total_turns_completed or 0) + turns_completed

        if response_time is not None:
            # 평균 응답 시간 계산
            current_avg = pylon_agent.average_response_time or 0
            total_turns = pylon_agent.total_turns_completed or 1
            new_avg = ((current_avg * (total_turns - 1)) + response_time) // total_turns
            pylon_agent.average_response_time = new_avg

        db.commit()
        db.refresh(pylon_agent)
        return pylon_agent

    def create_checkpoint(self, db: Session, id: int) -> PylonAgents | None:
        """체크포인트 생성"""
        from datetime import datetime
        pylon_agent = self.get_pylon_agent(db, id)
        if not pylon_agent:
            return None

        pylon_agent.last_checkpoint_at = datetime.now()
        pylon_agent.checkpoint_count = (pylon_agent.checkpoint_count or 0) + 1

        db.commit()
        db.refresh(pylon_agent)
        return pylon_agent
