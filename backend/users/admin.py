from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

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
    list_display = (
        'user',
        'country',
        'about',
        'post',
    )


@admin.register(ProfileDesigner)
class ProfileDesignerAdmin(admin.ModelAdmin):
    """
    Класс администратора профилей дизайнеров.

    """
    list_display = (
        'user',
        'education',
        'country',
        'get_instruments',
        'get_skills',
        'about',
        'get_specialization',
        'get_work_status',
        'get_language'
    )

    def get_instruments(self, obj):
        return ", ".join(
            instrument.name
            for instrument in obj.instruments.all()
        )
    get_instruments.short_description = 'Instruments'

    def get_skills(self, obj):
        return ", ".join([skill.name for skill in obj.skills.all()])
    get_skills.short_description = 'Skills'

    def get_specialization(self, obj):
        return ", ".join(
            specialization.name
            for specialization in obj.specialization.all()
        )
    get_specialization.short_description = 'Specialization'

    def get_language(self, obj):
        return ", ".join([language.name for language in obj.language.all()])
    get_language.short_description = 'Language'

    def get_work_status(self, obj):
        color = 'green' if obj.work_status else 'red'
        text = 'Ищет работу' if obj.work_status else 'Не ищет работу'
        return format_html('<span style="color: {};">{}</span>', color, text)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Класс администратора подписок.

    """
    list_display = ('user', 'author',)
