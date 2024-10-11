from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from pydantic import ValidationError

from users.service import UserService
from users.serializers import UserDumpSerializer
from users.schemas import UserCreate, UserLogin, Token, UserUpdate

from utils import auth as auth_utils
from utils import tokens as token_utils
from utils import password as password_utils
from utils.exceptions import CustomAPIException


class RegisterUserAPIView(APIView):
    def post(self, request: Request):
        try:
            user_data = UserCreate(**request.data)
        except ValidationError as e:
            raise CustomAPIException(
                detail={"message": e.errors()},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if UserService.get_user_by_email(email=user_data.email):
            raise CustomAPIException(
                detail={"message": "Пользователь с такой почтой уже существует"},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user = UserService.create_user(
            user_data=user_data
        )

        user.isLogin = True
        user.save()

        access_token = token_utils.create_access_token(user=user)
        refresh_token = token_utils.create_refresh_token(user=user)

        token_data = Token(
            user=UserDumpSerializer(user).data,
            access_token=access_token,
            refresh_token=refresh_token
        )

        return Response(
            data=token_data.model_dump(),
            status=status.HTTP_200_OK
        )


class LoginUserAPIView(APIView):
    def post(self, request: Request):
        try:
            user_data = UserLogin(**request.data)
        except ValidationError as e:
            raise CustomAPIException(
                detail={"message": e.errors()},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        user = UserService.get_user_by_email(email=user_data.email)
        
        if not user:
            raise CustomAPIException(
                detail={"message": "Пользователя с такой почтой не существует"},
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        if not password_utils.validate_password(
            password=user_data.password, 
            hashed_password=user.password.encode()
        ):
            raise CustomAPIException(
                detail={"message": "Неверный пароль"},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        user.isLogin = True
        user.save()

        access_token = token_utils.create_access_token(user=user)
        refresh_token = token_utils.create_refresh_token(user=user)

        token_data = Token(
            user=UserDumpSerializer(user).data,
            access_token=access_token,
            refresh_token=refresh_token
        )

        return Response(
            data=token_data.model_dump(),
            status=status.HTTP_200_OK
        )


class TokenRefreshAPIView(APIView):
    def get(self, request: Request):
        token = auth_utils.get_token_from_request(request=request)
        user = auth_utils.get_current_user_by_refresh(token=token)

        access_token = token_utils.create_access_token(user=user)

        token_data = Token(
            user=UserDumpSerializer(user).data,
            access_token=access_token
        )

        return Response(
            data=token_data.model_dump(exclude_none=True),
            status=status.HTTP_200_OK
        )


class UserMeAPIView(APIView):
    def get(self, request: Request):
        token = auth_utils.get_token_from_request(request=request)
        user = auth_utils.get_active_current_user(token=token)

        return Response(
            data=UserDumpSerializer(user).data,
            status=status.HTTP_200_OK
        )
    
    def patch(self, request: Request):
        token = auth_utils.get_token_from_request(request=request)
        user = auth_utils.get_active_current_user(token=token)

        try:
            user_data = UserUpdate(**request.data)
        except ValidationError as e:
            raise CustomAPIException(
                detail={"message": e.errors()},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        UserService.update_user(
            user_id=user.id,
            user_data=user_data
        )

        user = UserService.get_user_by_id(user_id=user.id)

        return Response(
            data=UserDumpSerializer(user).data,
            status=status.HTTP_200_OK
        )
    
    def delete(self, request: Request):
        token = auth_utils.get_token_from_request(request=request)
        user = auth_utils.get_active_current_user(token=token)

        if not UserService.delete_user(user_id=user.id):
            raise CustomAPIException(
                detail={"message": "Возникла ошибка удаления аккаунта"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response(
            data={"message": "Аккаунт успешно удалён"},
            status=status.HTTP_200_OK
        )


class LogoutUserAPIView(APIView):
    def get(self, request: Request):
        token = auth_utils.get_token_from_request(request=request)
        user = auth_utils.get_active_current_user(token=token)

        user.isLogin = False
        user.save()

        return Response(
            data={"message": "Вы разлогинены"},
            status=status.HTTP_200_OK
        )