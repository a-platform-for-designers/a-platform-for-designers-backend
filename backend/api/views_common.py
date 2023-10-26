from rest_framework import viewsets
from job.models import CaseImage, Comment
from .serializers_common import CaseImageSerializer, CommentSerializer

class CaseImageViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post')
    queryset = CaseImage.objects.all()
    serializer_class = CaseImageSerializer

class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post')
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
