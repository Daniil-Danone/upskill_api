from django.db import models
from django.utils import timezone   


from config.instance import (
    MALE, FEMALE, DEFAULT,
    STUDENT, TEACHER, ADMIN
)


class User(models.Model):

    SEX_CHOICES = [
        (MALE, "Мужской"),
        (FEMALE, "Женский"),
        (DEFAULT, "Не указано"),
    ]

    ROLE_CHOICES = [
        (STUDENT, "Ученик"),
        (TEACHER, "Преподаватель"),
        (ADMIN, "Администратор")
    ]

    id = models.AutoField(
        verbose_name="ID", primary_key=True
    )
    
    email = models.EmailField(
        verbose_name='Почта', unique=True, 
    )

    password = models.CharField(
        verbose_name="Пароль", blank=False, null=False
    )

    role = models.CharField(
        verbose_name="Роль", choices=ROLE_CHOICES, default=STUDENT
    )

    name = models.CharField(
        verbose_name='Имя', blank=False, null=False
    )

    surname = models.CharField(
        verbose_name='Фамилия', blank=False, null=False
    )

    birthDate = models.DateTimeField(
        verbose_name='Дата рождения', blank=True, null=True,
    )

    sex = models.CharField(
        verbose_name="Пол", choices=SEX_CHOICES, default=DEFAULT
    )

    phone = models.CharField(
        verbose_name='Телефон', blank=True, null=True
    )

    city = models.CharField(
        verbose_name="Город", blank=True, null=True
    )

    createdAt = models.DateTimeField(
        verbose_name='Дата регистрации',
        auto_now_add=True
    )

    isActive = models.BooleanField(default=True)

    isLogin = models.BooleanField(default=False)

    def __str__(self):
        return f"Пользователь: {self.surname} {self.name} - {self.email}"
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
