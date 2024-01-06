from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from api.serializers.instrument_serializers import InstrumentSerializer
from job.models import Instrument


class InstrumentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вью только для чтения для работы с инструментами.
    Позволяет получать список всех инструментов.
    Также позволяет получать инструмент по ID.

    """
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    pagination_class = None
    permission_classes = [AllowAny, ]
    search_fields = ['^name', ]

    @extend_schema(
        summary="Получение списка инструментов",
        description="Возвращает список всех инструментов, доступных в системе."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Получение деталей инструмента по ID",
        description="Возвращает подробную информацию об инструменте по ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
