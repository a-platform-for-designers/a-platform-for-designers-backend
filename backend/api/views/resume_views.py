from rest_framework import mixins
from rest_framework import viewsets

from api.permissions import IsAuthorOrReadOnly
from api.serializers.resume_serializers import ResumeReadSerializer
from api.serializers.resume_serializers import ResumeWriteSerializer
from job.models import Resume


class ResumeViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Resume.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ResumeReadSerializer
        return ResumeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
