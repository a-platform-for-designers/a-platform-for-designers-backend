from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscription, User
from .models import ProfileCustomer, ProfileDesigner


@admin.register(User)
class UserAdmin(UserAdmin):
    """
    Класс администратора пользователей.

    """
    ordering = ('email',)
    list_display = (
        'email', 'id',
        'first_name',
        'last_name',
        'photo',
        'date_joined',
        'is_customer',
    )
    list_filter = ('email', 'first_name')
    search_fields = (
        'email',
    )
    empty_value_display = '-пусто-'

    fieldsets = (
        (None, {'fields': (
            'email',
            'password'
        )}),
        ('Personal Info', {'fields': (
            'first_name',
            'last_name',
            'photo',
            'is_customer',
        )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),
        ('Important dates', {'fields': (
            'last_login',
        )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'photo',
                'is_customer',
            ),
        }),
    )


@admin.register(ProfileCustomer)
class ProfileCustomerAdmin(admin.ModelAdmin):
    """
    Класс администратора профилей покупателей.
    """

    list_display = ('user', 'post',)


@admin.register(ProfileDesigner)
class ProfileDesignerAdmin(admin.ModelAdmin):
    """
    Класс администратора профилей дизайнеров.
    """

    list_display = (
        'user',
        'education',
        'country',
        'hobby',
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Класс администратора подписок.

    """

    list_display = ('user', 'author',)
