from rest_framework import viewsets

from api.serializers.specialization_serializers import SpecializationSerializer
from job.models import Specialization


class SpecializationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SpecializationSerializer
    queryset = Specialization.objects.all()
