from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets, status, mixins
from api.permissions import IsAuthorOrReadOnly
from api.serializers.mentoring_serializers import MentoringWriteSerializer
from job.models import Mentoring


class MentoringViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    Вью для управления менторингом.
    Позволяет создавать дополнительную
    информацию по менторингу для дизайнеров.

    """
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Mentoring.objects.all()
    serializer_class = MentoringWriteSerializer

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=MentoringWriteSerializer,
                description="Информация по менторингу успешно создана"
            ),
        },
        summary="Создание информации по менторингу",
        description="Позволяет пользователям создавать и отправлять "
        "информацию по менторингу для дизайнеров."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
