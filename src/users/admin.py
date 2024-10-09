from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "role", "name", "surname", "createdAt", "isActive")


admin.site.register(User, UserAdmin)