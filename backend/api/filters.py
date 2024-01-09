from django_filters import rest_framework as filters

from job.models import Case, Order
from users.models import User
from job.models import Specialization, Instrument, Skill
from job.models import Sphere


class CaseFilter(filters.FilterSet):
    specialization_by_id = filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        field_name='specialization__id',
        to_field_name='id',
        label='Специализация по ID'
    )
    specialization_by_name = filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        field_name='specialization__name',
        to_field_name='name',
        label='Специализация по названию'
    )

    class Meta:
        model = Case
        fields = [
            'specialization_by_id',
            'specialization_by_name'
        ]


class DesignersFilter(filters.FilterSet):
    specialization_by_id = filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        field_name='profiledesigner__specialization__id',
        to_field_name='id',
        label='Специализация по ID'
    )
    specialization_by_name = filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        field_name='profiledesigner__specialization__name',
        to_field_name='name',
        label='Специализация по названию'
    )
    skills_by_id = filters.ModelMultipleChoiceFilter(
        queryset=Skill.objects.all(),
        field_name='profiledesigner__skills__id',
        to_field_name='id',
        label='Навыки по ID'
    )
    skills_by_name = filters.ModelMultipleChoiceFilter(
        queryset=Skill.objects.all(),
        field_name='profiledesigner__skills__name',
        to_field_name='name',
        label='Навыки по названию'
    )
    instruments_by_id = filters.ModelMultipleChoiceFilter(
        queryset=Instrument.objects.all(),
        field_name='profiledesigner__instruments__id',
        to_field_name='id',
        label='Инструменты по ID'
    )
    instruments_by_name = filters.ModelMultipleChoiceFilter(
        queryset=Instrument.objects.all(),
        field_name='profiledesigner__instruments__name',
        to_field_name='name',
        label='Инструменты по названию'
    )
    work_status = filters.BooleanFilter(
        field_name='profiledesigner__work_status',
    )

    class Meta:
        model = User
        fields = [
            'specialization_by_id', 'specialization_by_name',
            'skills_by_id', 'skills_by_name',
            'instruments_by_id', 'instruments_by_name',
            'work_status'
        ]


class OrdersFilter(filters.FilterSet):
    specialization_by_id = filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        field_name='specialization__id',
        to_field_name='id',
        label='Специализация по ID'
    )
    specialization_by_name = filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        field_name='specialization__name',
        to_field_name='name',
        label='Специализация по названию'
    )
    sphere_by_id = filters.ModelMultipleChoiceFilter(
        queryset=Sphere.objects.all(),
        field_name='sphere__id',
        to_field_name='id',
        label='Сфера по ID'
    )
    sphere_by_name = filters.ModelMultipleChoiceFilter(
        queryset=Sphere.objects.all(),
        field_name='sphere__name',
        to_field_name='name',
        label='Сфера по названию'
    )

    class Meta:
        model = Order
        fields = [
            'specialization_by_id',
            'specialization_by_name',
            'sphere_by_id',
            'sphere_by_name'
        ]
