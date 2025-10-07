from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models.chats import Chats

class ChatRepository:
    def get_chats(self, db: Session, session_id: str = None, send_type: str = None, limit: int = None) -> list[Chats]:
        """채팅 목록 조회 (필터 옵션)"""
        query = db.query(Chats)

        if session_id is not None:
            query = query.filter(Chats.session_id == session_id)
        if send_type is not None:
            query = query.filter(Chats.send_type == send_type)

        query = query.order_by(desc(Chats.created_at))

        if limit is not None:
            query = query.limit(limit)

        return query.all()

    def get_chat(self, db: Session, chat_id: int) -> Chats | None:
        """ID로 채팅 조회"""
        return db.query(Chats).filter(Chats.id == chat_id).first()

    def get_session_chats(self, db: Session, session_id: str, limit: int = None) -> list[Chats]:
        """특정 세션의 채팅 내역 조회 (최신순)"""
        query = (
            db.query(Chats)
            .filter(Chats.session_id == session_id)
            .order_by(Chats.created_at)
        )

        if limit is not None:
            query = query.limit(limit)

        return query.all()

    def get_latest_chat(self, db: Session, session_id: str) -> Chats | None:
        """세션의 가장 최근 채팅 조회"""
        return (
            db.query(Chats)
            .filter(Chats.session_id == session_id)
            .order_by(desc(Chats.created_at))
            .first()
        )

    def create(self,
               db: Session,
               session_id: str,
               send_type: str,
               send_id: str,
               chat_type: str,
               message: str,
               send_name: str = None,
               execution_status: str = "completed") -> Chats:
        """새 채팅 메시지 생성"""
        chat = Chats(
            session_id=session_id,
            send_type=send_type,
            send_id=send_id,
            send_name=send_name,
            chat_type=chat_type,
            message=message,
            execution_status=execution_status,
        )
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat

    def update(self,
               db: Session,
               chat_id: int,
               message: str = None,
               execution_status: str = None) -> Chats | None:
        """채팅 메시지 업데이트"""
        chat = self.get_chat(db, chat_id)
        if not chat:
            return None

        if message is not None:
            chat.message = message
        if execution_status is not None:
            chat.execution_status = execution_status

        db.commit()
        db.refresh(chat)
        return chat

    def delete(self, db: Session, chat_id: int) -> bool:
        """채팅 메시지 삭제"""
        chat = self.get_chat(db, chat_id)
        if not chat:
            return False

        db.delete(chat)
        db.commit()
        return True

    def delete_session_chats(self, db: Session, session_id: str) -> int:
        """특정 세션의 모든 채팅 삭제 (삭제된 개수 반환)"""
        count = db.query(Chats).filter(Chats.session_id == session_id).delete()
        db.commit()
        return count

    def get_chat_count(self, db: Session, session_id: str) -> int:
        """세션의 채팅 개수 조회"""
        return db.query(Chats).filter(Chats.session_id == session_id).count()

    def get_chats_by_sender(self, db: Session, session_id: str, send_id: str) -> list[Chats]:
        """특정 발신자의 채팅 내역 조회"""
        return (
            db.query(Chats)
            .filter(
                Chats.session_id == session_id,
                Chats.send_id == send_id
            )
            .order_by(Chats.created_at)
            .all()
        )

    def get_chats_by_type(self, db: Session, session_id: str, chat_type: str) -> list[Chats]:
        """특정 타입의 채팅 내역 조회"""
        return (
            db.query(Chats)
            .filter(
                Chats.session_id == session_id,
                Chats.chat_type == chat_type
            )
            .order_by(Chats.created_at)
            .all()
        )

    def update_execution_status(self, db: Session, chat_id: int, status: str) -> Chats | None:
        """채팅의 실행 상태 업데이트"""
        return self.update(db, chat_id, execution_status=status)
