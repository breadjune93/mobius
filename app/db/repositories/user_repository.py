import uuid
from sqlalchemy.orm import Session
from typing import Optional
from app.db.models.user import User

class UserRepository:
    def get_by_user_id(self, db: Session, user_id: str) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def create(self, db: Session, user_id: str, username: str, password_hash: str) -> User:
        user = User(
            id=user_id,
            role_id=1000,
            username=username,
            password=password_hash,
            is_active=True
        )

        db.add(user)
        return user