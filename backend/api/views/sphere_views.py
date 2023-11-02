from rest_framework import viewsets

from api.serializers.sphere_serializers import SphereSerializer
from job.models import Sphere


class SphereViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sphere.objects.all()
    serializer_class = SphereSerializer
