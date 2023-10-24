from django.contrib import admin

from .models import Case, Instrument, Skill, Favorite


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
        'status',
        'sphere',
        'instruments',
        'skills',
        'working_time',
        'description',
    )
    fields = (
        ('title', 'status', 'working_time',),
        ('description', 'skills',),
    )
    list_editable = ('skills',)
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