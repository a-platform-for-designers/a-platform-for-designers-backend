from django_filters import rest_framework as filters

from job.models import Case, RESUME_STATUS_CHOICES
from users.models import User


class CaseFilter(filters.FilterSet):
    """
    Фильтрация проектов по специализации.
    """

    specialization = filters.AllValuesMultipleFilter()

    class Meta:
        model = Case
        fields = ('specialization',)


class DesignersFilter(filters.FilterSet):
    """
    Фильтрация дизайнеров по специализации, стутусу резюме,
    скиллам и инструментам.
    """

    specialization = filters.AllValuesMultipleFilter(
        field_name='profiledesigner__specialization'
    )
    resume = filters.ChoiceFilter(
        field_name='resume__status',
        choices=RESUME_STATUS_CHOICES,
    )
    skills = filters.AllValuesMultipleFilter(
        field_name='resume__skills__id',
    )
    instruments = filters.AllValuesMultipleFilter(
        field_name='resume__instruments__id',
    )

    class Meta:
        model = User
        fields = ('specialization', 'resume', 'skills', 'instruments')
