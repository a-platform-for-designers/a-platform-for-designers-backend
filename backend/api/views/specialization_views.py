from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from api.serializers.specialization_serializers import SpecializationSerializer
from job.models import Specialization


class SpecializationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление только для чтения для работы со специализациями.
    Позволяет получать список всех специализаций или детальную
    информацию о конкретной специализации.

    """
    serializer_class = SpecializationSerializer
    queryset = Specialization.objects.all()

    @extend_schema(
        summary="Получение списка специализаций",
        description="Возвращает список всех специализаций."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Получение деталей специализации по ID",
        description="Возвращает подробную информацию о специализации по её ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
