from rest_framework import mixins, viewsets
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    LanguageSerializer, SpecializationSerializer, 
    ResumeReadSerializer, ResumeWriteSerializer,
    OrderSerializer
)
from job.models import Language, Order, Specialization


class SpecializationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SpecializationSerializer
    queryset = Specialization.objects.all()


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)