from sqlalchemy.orm import Session
from app.db.models.settings import Settings

class SettingRepository:
    def create(self, db: Session, user_id: str, theme_mode: str = "DARK") -> Settings:
        s = Settings(user_id=user_id, assistant="CLAUDE", theme_mode=theme_mode, chat_mode="PLAN")
        db.add(s)
        return s