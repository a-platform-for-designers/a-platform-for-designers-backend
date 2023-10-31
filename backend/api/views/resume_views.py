from api.permissions import IsAuthorOrReadOnly
from api.serializers.resume_serializers import ResumeReadSerializer, ResumeWriteSerializer


class ResumeViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ResumeReadSerializer
        return ResumeWriteSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
