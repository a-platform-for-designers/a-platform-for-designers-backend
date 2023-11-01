from django.contrib import admin
from .models import Case, Instrument, Skill, Favorite, Chat, Message, CaseImage


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
    )


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'author',
        'sphere',
        # 'instruments',
        # 'skills',
        'working_term',
        'description',
    )
    fields = (
        ('title', 'working_term',),
        ('description', 'skills', 'author'),
    )
    # list_editable = ('skills',)
    search_fields = ('title',)
    list_filter = ('sphere', 'title', 'skills',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'case',
    )


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('pk', 'initiator', 'receiver')
    search_fields = ('initiator', 'receiver')
    list_filter = ('initiator', 'receiver')
    empty_value_display = '-пусто-'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'text', 'pub_date')
    search_fields = ('chat', 'sender', 'text')
    list_filter = ('chat', 'sender', 'pub_date')
    empty_value_display = '-пусто-'


@admin.register(CaseImage)
class CaseImageAdmin(admin.ModelAdmin):
    list_display = (
        'case',
        'picture',
        'name',
        'description'
    )
