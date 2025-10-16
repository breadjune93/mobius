from sqlalchemy.orm import Session
from app.db.repositories.agent_repository import AgentRepository
from app.db.repositories.chat_repository import ChatRepository
from app.db.models.agents import Agents
from app.db.models.chats import Chats
from typing import List, Optional
import uuid

class PylonService:
    def __init__(self,
                 agent_repository: AgentRepository,
                 chat_repository: ChatRepository):
        self.agent_repository = agent_repository
        self.chat_repository = chat_repository

    # ============================================
    # Agent Methods
    # ============================================
    def get_agents(self, db: Session, is_active: bool = None) -> List[Agents]:
        """에이전트 목록 조회"""
        return self.agent_repository.get_agents(db, is_active)

    def get_agent(self, db: Session, agent_id: str) -> Agents | None:
        """에이전트 조회"""
        return self.agent_repository.get_agent(db, agent_id)

    def create_agent(self,
                     db: Session,
                     name: str,
                     instructions: str,
                     assistant: str = "anthropic",
                     model: str = "claude-sonnet-4-5",
                     max_turns: int = 50,
                     temperature: float = 1.0,
                     allowed_tools: dict = None,
                     disallowed_tools: dict = None,
                     mcp_servers: dict = None) -> Agents:
        """새 에이전트 생성"""
        agent_id = str(uuid.uuid4())
        return self.agent_repository.create(
            db=db,
            agent_id=agent_id,
            name=name,
            instructions=instructions,
            assistant=assistant,
            model=model,
            max_turns=max_turns,
            temperature=temperature,
            allowed_tools=allowed_tools,
            disallowed_tools=disallowed_tools,
            mcp_servers=mcp_servers
        )

    def update_agent(self,
                     db: Session,
                     agent_id: str,
                     **kwargs) -> Agents | None:
        """에이전트 업데이트"""
        return self.agent_repository.update(db, agent_id, **kwargs)

    def delete_agent(self, db: Session, agent_id: str) -> bool:
        """에이전트 삭제"""
        return self.agent_repository.delete(db, agent_id)

    # ============================================
    # Chat Methods
    # ============================================
    def get_chats(self, db: Session, session_id: str, limit: int = None) -> List[Chats]:
        """채팅 내역 조회"""
        return self.chat_repository.get_session_chats(db, session_id, limit)

    def get_chat(self, db: Session, chat_id: int) -> Chats | None:
        """채팅 조회"""
        return self.chat_repository.get_chat(db, chat_id)

    def create_chat(self,
                    db: Session,
                    session_id: str,
                    send_type: str,
                    send_id: str,
                    chat_type: str,
                    message: str,
                    send_name: str = None,
                    execution_status: str = "completed") -> Chats:
        """채팅 메시지 생성"""
        return self.chat_repository.create(
            db=db,
            session_id=session_id,
            send_type=send_type,
            send_id=send_id,
            send_name=send_name,
            chat_type=chat_type,
            message=message,
            execution_status=execution_status
        )

    def update_chat_status(self, db: Session, chat_id: int, status: str) -> Chats | None:
        """채팅 상태 업데이트"""
        return self.chat_repository.update_execution_status(db, chat_id, status)

    def delete_chat(self, db: Session, chat_id: int) -> bool:
        """채팅 삭제"""
        return self.chat_repository.delete(db, chat_id)

    def get_chat_count(self, db: Session, session_id: str) -> int:
        """세션의 채팅 개수 조회"""
        return self.chat_repository.get_chat_count(db, session_id)
