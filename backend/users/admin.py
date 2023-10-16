from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    """
    Класс администратора пользователей.

    """

    list_display = (
        'email', 'id',
        'username',
        'first_name',
        'last_name',
    )
    list_filter = ('email', 'first_name')
    search_fields = (
        'email',
        'username',
    )
    empty_value_display = '-пусто-'
