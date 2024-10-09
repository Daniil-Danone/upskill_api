from rest_framework.serializers import ModelSerializer

from users.models import User


class UserDumpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "email", "role", "name", "surname", "birthDate", "sex", "phone", "city", "createdAt"
        ]

class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email", "password", "name", "surname", "birthDate", "sex"
        ]


class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email", "password",
        ]
