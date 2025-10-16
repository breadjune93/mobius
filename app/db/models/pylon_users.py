from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class PylonUsers(Base):
    __tablename__ = "pylon_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pylon_id = Column(Integer, ForeignKey("pylons.id"), nullable=False)
    user_id = Column(String(50), nullable=False)
    user_role = Column(String(50), nullable=False)
    pylon_role = Column(String(50), nullable=False, default="owner")
    user_image_url = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
