from rest_framework.serializers import ModelSerializer

from users.models import User


class UserDumpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "email", "role", "name", "surname", "birth_date", "sex", "phone", "city", "created_at"
        ]

class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email", "password", "name", "surname", "birth_date", "sex"
        ]


class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email", "password",
        ]
