from rest_framework import viewsets
from job.models import CaseImage
from .serializers import CaseImageSerializer

class CaseImageViewSet(viewsets.ModelViewSet):
    queryset = CaseImage.objects.all()
    serializer_class = CaseImageSerializer
