from django_filters import rest_framework as filters

from job.models import Case, Order
from users.models import User
from job.models import Specialization, Instrument, Skill
from job.models import Sphere


class CaseFilter(filters.FilterSet):
    """
    Фильтрация проектов по специализации.

    """
    specialization = filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        field_name='specialization',
        to_field_name='id',
        label='Специализация по ID'
    )

    # Дополнительный фильтр по имени
    specialization_name = filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        field_name='specialization__name',
        to_field_name='name',
        label='Специализация по имени'
    )

    class Meta:
        model = Case
        fields = ['specialization', 'specialization_name']


class DesignersFilter(filters.FilterSet):
    """
    Фильтрация дизайнеров по специализации, стутусу резюме,
    скиллам и инструментам.

    """
    specialization = filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        field_name='profiledesigner__specialization',
        to_field_name='id'
    )
    skills = filters.ModelMultipleChoiceFilter(
        queryset=Skill.objects.all(),
        field_name='profiledesigner__skills',
        to_field_name='id'
    )
    instruments = filters.ModelMultipleChoiceFilter(
        queryset=Instrument.objects.all(),
        field_name='profiledesigner__instruments',
        to_field_name='id'
    )

    # Дополнительные фильтры по имени
    specialization_name = filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        field_name='profiledesigner__specialization__name',
        to_field_name='name',
        label='Специализация по имени'
    )
    skills_name = filters.ModelMultipleChoiceFilter(
        queryset=Skill.objects.all(),
        field_name='profiledesigner__skills__name',
        to_field_name='name',
        label='Навыки по имени'
    )
    instruments_name = filters.ModelMultipleChoiceFilter(
        queryset=Instrument.objects.all(),
        field_name='profiledesigner__instruments__name',
        to_field_name='name',
        label='Инструменты по имени'
    )

    work_status = filters.BooleanFilter(
        field_name='profiledesigner__work_status'
    )

    class Meta:
        model = User
        fields = [
            'specialization', 'specialization_name',
            'skills', 'skills_name',
            'instruments', 'instruments_name',
            'work_status'
        ]


class OrdersFilter(filters.FilterSet):
    """
    Фильтрация заказов по специализации и сфере.

    """
    specialization = filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        field_name='specialization',
        to_field_name='id',
        label='Специализация по ID'
    )
    sphere = filters.ModelMultipleChoiceFilter(
        queryset=Sphere.objects.all(),
        field_name='sphere',
        to_field_name='id',
        label='Сфера по ID'
    )

    # Дополнительные фильтры по имени
    specialization_name = filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        field_name='specialization__name',
        to_field_name='name',
        label='Специализация по имени'
    )
    sphere_name = filters.ModelMultipleChoiceFilter(
        queryset=Sphere.objects.all(),
        field_name='sphere__name',
        to_field_name='name',
        label='Сфера по имени'
    )

    class Meta:
        model = Order
        fields = [
            'specialization', 'specialization_name',
            'sphere', 'sphere_name'
        ]
