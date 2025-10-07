from sqlalchemy.orm import Session
from app.db.models.agents import Agents

class AgentRepository:
    def get_agents(self, db: Session, is_active: bool = None) -> list[Agents]:
        """모든 에이전트 조회 (활성 상태 필터 옵션)"""
        query = db.query(Agents)
        if is_active is not None:
            query = query.filter(Agents.is_active == is_active)
        return query.all()

    def get_agent(self, db: Session, agent_id: str) -> Agents | None:
        """ID로 에이전트 조회"""
        return db.query(Agents).filter(Agents.id == agent_id).first()

    def get_agent_by_name(self, db: Session, name: str) -> Agents | None:
        """이름으로 에이전트 조회"""
        return db.query(Agents).filter(Agents.name == name).first()

    def create(self,
               db: Session,
               agent_id: str,
               name: str,
               instructions: str,
               is_active: bool = True,
               assistant: str = "anthropic",
               model: str = "claude-sonnet-4-5",
               max_turns: int = 50,
               temperature: float = 1.0,
               allowed_tools: dict = None,
               disallowed_tools: dict = None,
               mcp_servers: dict = None) -> Agents:
        """새 에이전트 생성"""
        agent = Agents(
            id=agent_id,
            name=name,
            is_active=is_active,
            assistant=assistant,
            model=model,
            instructions=instructions,
            max_turns=max_turns,
            temperature=temperature,
            allowed_tools=allowed_tools,
            disallowed_tools=disallowed_tools,
            mcp_servers=mcp_servers,
        )
        db.add(agent)
        db.commit()
        db.refresh(agent)
        return agent

    def update(self,
               db: Session,
               agent_id: str,
               name: str | None = None,
               is_active: bool | None = None,
               assistant: str | None = None,
               model: str | None = None,
               instructions: str | None = None,
               max_turns: int | None = None,
               temperature: float | None = None,
               allowed_tools: dict | None = None,
               disallowed_tools: dict | None = None,
               mcp_servers: dict | None = None) -> Agents | None:
        """에이전트 업데이트"""
        agent = self.get_agent(db, agent_id)
        if not agent:
            return None

        if name is not None:
            agent.name = name
        if is_active is not None:
            agent.is_active = is_active
        if assistant is not None:
            agent.assistant = assistant
        if model is not None:
            agent.model = model
        if instructions is not None:
            agent.instructions = instructions
        if max_turns is not None:
            agent.max_turns = max_turns
        if temperature is not None:
            agent.temperature = temperature
        if allowed_tools is not None:
            agent.allowed_tools = allowed_tools
        if disallowed_tools is not None:
            agent.disallowed_tools = disallowed_tools
        if mcp_servers is not None:
            agent.mcp_servers = mcp_servers

        db.commit()
        db.refresh(agent)
        return agent

    def delete(self, db: Session, agent_id: str) -> bool:
        """에이전트 삭제"""
        agent = self.get_agent(db, agent_id)
        if not agent:
            return False

        db.delete(agent)
        db.commit()
        return True

    def deactivate(self, db: Session, agent_id: str) -> Agents | None:
        """에이전트 비활성화"""
        return self.update(db, agent_id, is_active=False)

    def activate(self, db: Session, agent_id: str) -> Agents | None:
        """에이전트 활성화"""
        return self.update(db, agent_id, is_active=True)
