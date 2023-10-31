from api.serializers.sphere_serializers import SphereSerializer
from job.models import Sphere


class SphereViewSet(viewsets.ModelViewSet):
    http_method_names = ('get')
    queryset = Sphere.objects.all()
    serializer_class = SphereSerializer