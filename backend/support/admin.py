from django.contrib import admin
from django.utils.text import Truncator
from .models import SupportTicket


@admin.action(description='Отметить как прочитанные')
def make_read(modeladmin, request, queryset):
    queryset.update(is_read=True)


@admin.action(description='Отметить как непрочитанные')
def make_unread(modeladmin, request, queryset):
    queryset.update(is_read=False)


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    """
    Модель для прочтения сообщений в поддержку.

    """
    def truncated_message(self, obj):
        return Truncator(obj.message).chars(300)

    truncated_message.short_description = "Сообщение"

    list_display = (
        'subject',
        'name',
        'email',
        'truncated_message',
        'is_read',
        'created_at'
    )
    list_filter = (
        'is_read',
        'created_at'
    )
    search_fields = (
        'name',
        'email',
        'subject'
    )
    list_editable = ('is_read',)
    readonly_fields = (
        'name',
        'email',
        'subject',
        'message',
        'created_at'
    )
    actions = [make_read, make_unread]
