import hashlib
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.db.repositories.user_repository import UserRepository
from app.db.repositories.setting_repository import SettingRepository

class AuthService:
    def __init__(self, user_repository: UserRepository, setting_repository: SettingRepository):
        self.user_repository = user_repository
        self.setting_repository = setting_repository

    def signup(self, db: Session, user_id: str, username, password: str, theme: str):
        if self.user_repository.get_by_user_id(db, user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 존재하는 사용자명입니다.")

        try:
            user = self.user_repository.create(db, user_id, username, hash_password(password))
            self.setting_repository.create(db, user.id, theme)
            db.commit()
            db.refresh(user)

            return {
                "is_succeed": True
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"회원가입 실패: {str(e)}")


    def login(self, db: Session, user_id: str, password: str):
        user = self.user_repository.get_by_user_id(db, user_id)

        if not user or not verify_password(password, user.password):
            print(f"비밀번호 불일치")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="계정이 일치하지 않습니다.")

        try:
            # 토큰 생성
            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id)

            # refresh_token을 users 테이블에 저장
            user.refresh_token = refresh_token
            db.commit()
            db.refresh(user)

            return {
                "user_id": user.id,
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="로그인에 실패했습니다.")