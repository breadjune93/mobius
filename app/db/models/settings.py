from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), nullable=False)
    assistant = Column(String(50), nullable=False, default="CLAUDE")
    theme_mode = Column(String(50), nullable=False, default="DARK")
    chat_mode = Column(String(50), nullable=False, default="PLAN")