from django.contrib import admin
from .models import (
    Case, Instrument, Skill, FavoriteCase, Chat, Message, Sphere,
    Specialization, Order, CaseImage, FavoriteOrder, Resume, Language
)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'id',
        'about',
        'status'
    )


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
    )


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
    )


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
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


class CaseImageInline(admin.TabularInline):

    model = CaseImage
    extra = 1


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'author',
        'sphere',
        'working_term',
        'description',
        'specialization',
    )
    fields = (
        ('title', 'working_term',),
        ('description', 'author', 'avatar'),
        'specialization',
        'sphere',
        'instruments',
    )
    inlines = [CaseImageInline]
    search_fields = ('title',)
    list_filter = ('sphere', 'title', )
    empty_value_display = '-пусто-'


@admin.register(FavoriteCase)
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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'title',
        'specialization',
        'payment',
        'sphere',
        'description'
    )


@admin.register(Sphere)
class SphereAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
    )


@admin.register(FavoriteOrder)
class FavoriteOrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'order',
        'id',
    )
