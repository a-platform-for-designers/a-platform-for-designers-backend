from rest_framework.permissions import AllowAny

from api.serializers.skill_serializers import SkillSerializer
from job.models import Skill

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    pagination_class = None
    permission_classes = [AllowAny, ]