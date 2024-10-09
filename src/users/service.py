from typing import Dict
from users.models import User
from users.schemas import UserCreate, UserCreateDB, UserUpdate

from utils.logger import user_logger
from utils import password as password_utils


class UserService:

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        try:
            return User.objects.get(pk=user_id)
        except Exception as e:
            user_logger.error(f"[GET by ID] Error: {e}")
            return None
        
    @staticmethod
    def get_user_by_email(email: str) -> User:
        try:
            return User.objects.get(email=email)
        except Exception as e:
            user_logger.error(f"[GET by EMAIL] Error: {e}")
            return None

    @staticmethod
    def create_user(user_data: UserCreate) -> User:
        try:
            hashed_password: bytes = password_utils.hash_password(
                password=user_data.password
            )

            data = UserCreateDB(
                email=user_data.email,
                password=hashed_password.decode(),
                name=user_data.name,
                surname=user_data.surname,
                birthDate=user_data.birthDate,
                sex=user_data.sex
            )

            return User.objects.create(**data.model_dump())

        except Exception as e:
            user_logger.error(f"[CREATE] Error: {e}")
            return None
        
    @staticmethod
    def update_user(user_id: int, user_data: UserUpdate) -> User:
        try:
            user_logger.error(f"[UPDATE] {user_data.model_dump(exclude_none=True)}")
            return User.objects.filter(id=user_id).update(**user_data.model_dump(exclude_none=True))
        except Exception as e:
            user_logger.error(f"[UPDATE] Error: {e}")
            return None
    
    @staticmethod
    def delete_user(user_id: int) -> bool:
        try:
            User.objects.filter(id=user_id).delete()
            return True
        except Exception as e:
            user_logger.error(f"[DELETE] Error: {e}")
            return False