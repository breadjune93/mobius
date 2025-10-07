from sqlalchemy.orm import Session
from app.db.models.sessions import Sessions

class SessionRepository:
    def get_session(self, db: Session, session_id: str) -> Sessions | None:
        """ID로 세션 조회"""
        return db.query(Sessions).filter(Sessions.id == session_id).first()

    def get_active_session(self, db: Session, pylon_id: int, agent_id: str) -> Sessions | None:
        """특정 파일런과 에이전트의 활성 세션 조회"""
        return (
            db.query(Sessions)
            .filter(
                Sessions.pylon_id == pylon_id,
                Sessions.agent_id == agent_id,
                Sessions.is_active == True,
                Sessions.session_state == "active"
            )
            .first()
        )

    def create(self,
               db: Session,
               session_id: str,
               pylon_id: int,
               agent_id: str,
               working_directory: str,
               is_active: bool = True,
               session_state: str = "active",
               fork_id: str = None,
               claude_md_content: str = None,
               mcp_servers: dict = None,
               subagents_enabled: bool = False,
               active_subagents: dict = None,
               context_token_count: int = 0,
               memory_enabled: bool = False,
               memory_directory: str = None,
               allowed_tools: dict = None,
               disallowed_tools: dict = None) -> Sessions:
        """새 세션 생성"""
        session = Sessions(
            id=session_id,
            pylon_id=pylon_id,
            agent_id=agent_id,
            is_active=is_active,
            session_state=session_state,
            working_directory=working_directory,
            fork_id=fork_id,
            claude_md_content=claude_md_content,
            mcp_servers=mcp_servers,
            subagents_enabled=subagents_enabled,
            active_subagents=active_subagents,
            context_token_count=context_token_count,
            memory_enabled=memory_enabled,
            memory_directory=memory_directory,
            allowed_tools=allowed_tools,
            disallowed_tools=disallowed_tools,
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    def update(self,
               db: Session,
               session_id: str,
               is_active: bool | None = None,
               session_state: str | None = None,
               working_directory: str | None = None,
               fork_id: str | None = None,
               claude_md_content: str | None = None,
               mcp_servers: dict | None = None,
               subagents_enabled: bool | None = None,
               active_subagents: dict | None = None,
               context_token_count: int | None = None,
               memory_enabled: bool | None = None,
               memory_directory: str | None = None,
               allowed_tools: dict | None = None,
               disallowed_tools: dict | None = None,
               total_tokens_used: int | None = None,
               total_tool_calls: int | None = None,
               total_turns_completed: int | None = None,
               average_response_time: int | None = None) -> Sessions | None:
        """세션 업데이트"""
        session = self.get_session(db, session_id)
        if not session:
            return None

        if is_active is not None:
            session.is_active = is_active
        if session_state is not None:
            session.session_state = session_state
        if working_directory is not None:
            session.working_directory = working_directory
        if fork_id is not None:
            session.fork_id = fork_id
        if claude_md_content is not None:
            session.claude_md_content = claude_md_content
        if mcp_servers is not None:
            session.mcp_servers = mcp_servers
        if subagents_enabled is not None:
            session.subagents_enabled = subagents_enabled
        if active_subagents is not None:
            session.active_subagents = active_subagents
        if context_token_count is not None:
            session.context_token_count = context_token_count
        if memory_enabled is not None:
            session.memory_enabled = memory_enabled
        if memory_directory is not None:
            session.memory_directory = memory_directory
        if allowed_tools is not None:
            session.allowed_tools = allowed_tools
        if disallowed_tools is not None:
            session.disallowed_tools = disallowed_tools
        if total_tokens_used is not None:
            session.total_tokens_used = total_tokens_used
        if total_tool_calls is not None:
            session.total_tool_calls = total_tool_calls
        if total_turns_completed is not None:
            session.total_turns_completed = total_turns_completed
        if average_response_time is not None:
            session.average_response_time = average_response_time

        db.commit()
        db.refresh(session)
        return session

    def delete(self, db: Session, session_id: str) -> bool:
        """세션 삭제"""
        session = self.get_session(db, session_id)
        if not session:
            return False

        db.delete(session)
        db.commit()
        return True

    def deactivate(self, db: Session, session_id: str) -> Sessions | None:
        """세션 비활성화"""
        return self.update(db, session_id, is_active=False, session_state="inactive")

    def activate(self, db: Session, session_id: str) -> Sessions | None:
        """세션 활성화"""
        return self.update(db, session_id, is_active=True, session_state="active")

    def update_stats(self,
                     db: Session,
                     session_id: str,
                     tokens_used: int = 0,
                     tool_calls: int = 0,
                     turns_completed: int = 0,
                     response_time: int = None) -> Sessions | None:
        """세션 통계 업데이트"""
        session = self.get_session(db, session_id)
        if not session:
            return None

        session.total_tokens_used = (session.total_tokens_used or 0) + tokens_used
        session.total_tool_calls = (session.total_tool_calls or 0) + tool_calls
        session.total_turns_completed = (session.total_turns_completed or 0) + turns_completed

        if response_time is not None:
            # 평균 응답 시간 계산
            current_avg = session.average_response_time or 0
            total_turns = session.total_turns_completed or 1
            new_avg = ((current_avg * (total_turns - 1)) + response_time) // total_turns
            session.average_response_time = new_avg

        db.commit()
        db.refresh(session)
        return session

    def create_checkpoint(self, db: Session, session_id: str) -> Sessions | None:
        """세션 체크포인트 생성"""
        from datetime import datetime
        session = self.get_session(db, session_id)
        if not session:
            return None

        session.last_checkpoint_at = datetime.now()
        session.checkpoint_count = (session.checkpoint_count or 0) + 1

        db.commit()
        db.refresh(session)
        return session
