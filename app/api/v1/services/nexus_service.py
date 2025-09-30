import hashlib
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.db.repositories.user_repository import UserRepository
from app.db.repositories.setting_repository import SettingRepository

class NexusService:
    def __init__(self, user_repository: UserRepository, setting_repository: SettingRepository):
        self.user_repository = user_repository
        self.setting_repository = setting_repository

    def get_workspace(self, ):

    def create_workspace(self):

    def update_workspace(self, db: Session, user_id: str, password: str):

    def delete_workspace(self):
