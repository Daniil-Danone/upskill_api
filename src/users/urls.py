from django.urls import path
from users.views import (
    UserMeAPIView,
    LoginUserAPIView, 
    RegisterUserAPIView, 
    TokenRefreshAPIView,
)

urlpatterns = [
    path('me', UserMeAPIView.as_view(), name='user_me'),
    path('login', LoginUserAPIView.as_view(), name='login_user'),
    path('register', RegisterUserAPIView.as_view(), name='register_user'),
    path('token/refresh', TokenRefreshAPIView.as_view(), name='refresh_token')
]

