from rest_framework import mixins
from rest_framework import viewsets

from api.permissions import IsAuthorOrReadOnly
from api.serializers.mentoring_serializers import MentoringWriteSerializer
from job.models import Mentoring


class MentoringViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Mentoring.objects.all()
    serializer_class = MentoringWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
