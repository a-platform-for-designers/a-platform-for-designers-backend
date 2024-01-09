from django_filters import rest_framework as filters

from job.models import Case, Order
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
    work_status = filters.BooleanFilter(
        field_name='profiledesigner__work_status',
    )
    skills = filters.AllValuesMultipleFilter(
        field_name='profiledesigner__skills',
    )
    instruments = filters.AllValuesMultipleFilter(
        field_name='profiledesigner__instruments',
    )

    class Meta:
        model = User
        fields = ('specialization', 'work_status', 'skills', 'instruments')


class OrdersFilter(filters.FilterSet):
    """
    Фильтрация заказов по специализации и сфере.
    """

    specialization = filters.AllValuesMultipleFilter()
    sphere = filters.AllValuesMultipleFilter()

    class Meta:
        model = Order
        fields = ('specialization', 'sphere')
