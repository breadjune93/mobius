from sqlalchemy.orm import Session
from app.db.models.pylon_agents import PylonAgents

class PylonAgentsRepository:
    def get_agent_by_pylon(self, db: Session, pylon_id: int) -> list[type[PylonAgents]]:
        """ID로 pylon_agent 조회"""
        return (
            db.query(PylonAgents)
            .filter(PylonAgents.pylon_id == pylon_id)
            .all()
        )

    def get_agent_by_id(self, db: Session, pylon_agent_id: int) -> PylonAgents | None:
        """특정 pylon과 agent의 관계 조회"""
        return (
            db.query(PylonAgents)
            .filter(PylonAgents.id == pylon_agent_id)
            .first()
        )

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

    def update_agent(self,
               db: Session,
               pylon_agent_id: int,
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
        pylon_agent = self.get_agent_by_id(db, pylon_agent_id)
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

    def delete_agent(self, db: Session, pylon_agent_id: int) -> bool:
        """pylon_agent 삭제"""
        pylon_agent = self.get_agent_by_id(db, pylon_agent_id)
        if not pylon_agent:
            return False

        db.delete(pylon_agent)
        db.commit()
        return True
