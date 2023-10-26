from rest_framework import viewsets
from job.models import CaseImage
from .serializers_common import CaseImageSerializer

class CaseImageViewSet(viewsets.ModelViewSet):
    queryset = CaseImage.objects.all()
    serializer_class = CaseImageSerializer
