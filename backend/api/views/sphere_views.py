# from drf_spectacular.utils import extend_schema
# from rest_framework import viewsets

# from api.serializers.sphere_serializers import SphereSerializer
# from job.models import Sphere


# class SphereViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     Представление для просмотра списка сфер или отдельной сферы.

#     """
#     queryset = Sphere.objects.all()
#     serializer_class = SphereSerializer

#     @extend_schema(
#         summary="Получение списка сфер",
#         description="Возвращает список всех сфер, доступных в системе."
#     )
#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)

#     @extend_schema(
#         summary="Получение деталей сферы по ID",
#         description="Возвращает подробную информацию о сфере по её ID."
#     )
#     def retrieve(self, request, *args, **kwargs):
#         return super().retrieve(request, *args, **kwargs)
