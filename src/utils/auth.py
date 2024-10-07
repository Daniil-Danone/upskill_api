from typing import Dict, Union
from rest_framework import status
from rest_framework.request import Request
from jwt import InvalidTokenError, ExpiredSignatureError

from config.instance import ADMIN, STUDENT, TOKEN_TYPE

from users.models import User
from users.service import UserService

from utils.tokens import decode_jwt
from utils.exceptions import CustomAPIException


def get_current_token_payload(token: str) -> Dict:
    try:
        payload: Dict = decode_jwt(token=token)

        return payload
    
    except ExpiredSignatureError as e:
        raise CustomAPIException(
            detail={"message": "Время жизни токена истекло"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    except InvalidTokenError as e:
        raise CustomAPIException(
            detail={
                "message": "Неверный токен"
            },
            status_code=status.HTTP_401_UNAUTHORIZED
        )


def validate_token(payload: Dict, token_type: str) -> bool:
    current_token_type: str = payload.get("type")

    if current_token_type != token_type:
        raise CustomAPIException(
            detail={
                "message": f"Неверный формат токена: '{current_token_type}' | ожидался: '{token_type}'"
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return True


def get_user_by_token(payload: Dict) -> User:
    user_id: Union[int, None] = payload.get("user_id")

    if not user_id:
        raise CustomAPIException(
            detail={
                "message": f"Пользователь с ID {user_id} не найден"
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )

    user = UserService.get_user_by_id(user_id=user_id)
    return user


def get_current_user(token: str) -> User:
    payload = get_current_token_payload(token=token)
    validate_token(payload=payload, token_type="access")

    return get_user_by_token(payload=payload)


def get_current_user_by_refresh(token: str) -> User:
    payload = get_current_token_payload(token=token)
    validate_token(payload=payload, token_type="refresh")
    return get_user_by_token(payload=payload)


def get_active_current_user(token: str) -> User:
    user = get_current_user(token=token)

    if not user:
        raise CustomAPIException(
            detail={
                "message": f"Пользователя не существует"
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )
    
    if not user.is_active:
        raise CustomAPIException(
            detail={
                "message": f"Пользователь {user.id} заблокирован"
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return user


def get_teacher_user(token: str) -> User:
    user = get_active_current_user(token=token)

    if user.role == STUDENT:
        raise CustomAPIException(
            detail={
                "message": f"У пользователя {user.email} недостаточно прав"
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return user


def get_admin_user(token: str) -> User:
    user = get_active_current_user(token=token)

    if not user.role == ADMIN:
        raise CustomAPIException(
            detail={
                "message": f"У пользователя {user.email} недостаточно прав"
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return user


def get_token_from_request(request: Request) -> str:
    bearer_token: str = request.headers.get("Authorization", None)

    if not bearer_token:
        raise CustomAPIException(
            detail={"message": "Не указан токен доступа"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    token_type, token = bearer_token.split()

    if token_type != TOKEN_TYPE:
        raise CustomAPIException(
            detail={"message": "Неверный формат токена"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    return token