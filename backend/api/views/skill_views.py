from rest_framework.permissions import AllowAny
from rest_framework import viewsets

from drf_spectacular.utils import extend_schema

from api.serializers.skill_serializers import SkillSerializer
from job.models import Skill


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вью только для работы с навыками. Позволяет получать
    список всех навыков.
    Также позволяет получать навык по ID.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    pagination_class = None
    permission_classes = [AllowAny,]

    @extend_schema(summary="Получить список всех навыков")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Получить название навыка по ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
