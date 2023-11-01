from django.contrib import admin

from .models import Case, Instrument, Skill, Sphere, FavoriteCase


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

    fields = ('name',)


@admin.register(Sphere)
class SphereAdmin(admin.ModelAdmin):
    list_display = (
        # 'name',
        'id',
    )


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'author',
        # 'sphere',
        # 'instruments',
        # 'skills',
        'working_term',
        'description',
        'pub_date'
    )
    fields = (
        ('title', 'skills', 'instruments', 'description', 'sphere'),
        ('working_term', 'author', ),
    )
    # list_editable = ('skills',)
    search_fields = ('title',)
    list_filter = ('sphere', 'title', 'skills',)
    empty_value_display = '-пусто-'


# @admin.register(CaseImage)
# class CaseImageAdmin(admin.ModelAdmin):
#     list_display = (
#         # 'pk',
#         # 'title',
#         # 'author',
#         # 'sphere',
#         # # 'instruments',
#         # # 'skills',
#         # 'working_term',
#         # 'description',
#     )

@admin.register(FavoriteCase)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'case',
    )
