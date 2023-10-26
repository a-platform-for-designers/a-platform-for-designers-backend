from rest_framework import viewsets
from job.models import CaseImage, Comment, Sphere
from .serializers_common import CaseImageSerializer, CommentSerializer, SphereSerializer


class CaseImageViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post')
    queryset = CaseImage.objects.all()
    serializer_class = CaseImageSerializer


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post')
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class SphereViewSet(viewsets.ModelViewSet):
    http_method_names = ('get')
    queryset = Sphere.objects.all()
    serializer_class = SphereSerializer
