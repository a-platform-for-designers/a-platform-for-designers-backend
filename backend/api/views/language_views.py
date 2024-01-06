from rest_framework import viewsets

from drf_spectacular.utils import extend_schema

from api.serializers.language_serializers import LanguageSerializer
from job.models import Language


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вью только для чтения для работы с языками. Позволяет получать
    список всех языков.
    Также позволяет получать язык по ID.

    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    @extend_schema(
        summary="Получение списка языков",
        description="Возвращает список всех языков, доступных в системе."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Получение деталей языка по ID",
        description="Возвращает подробную информацию о языке по его ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
