from django_filters.rest_framework import DjangoFilterBackend
# from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.filters import CaseFilter
from api.pagination import LimitPageNumberPagination
# from api.serializers.caseimage_serializers import CaseImageSerializer
from api.serializers.case_serializers import (
    CaseSerializer, CaseCreateSerializer
)
from job.models import Case
from api.permissions import IsAuthorOrReadOnly


class CaseViewSet(ModelViewSet):
    """
    Вью для работы с проектами авторов.

    list/retrieve:
    Возвращает список всех кейсов, упорядоченных
    по дате создания и другим параметрам.
    Также позволяет получать кейс по ID.

    """
    http_method_names = ['get', 'post', 'delete']
    queryset = Case.objects.all()
    pagination_class = LimitPageNumberPagination
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CaseFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CaseSerializer
        return CaseCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(
        summary="Создание проекта.",
        description="Создает новый проект. Доступ запрещен для заказчиков.",
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description="Проект успешно создан."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Неавторизованный доступ."
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="Заказчик не может создавать кейс."
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        if request.user.is_customer:
            return Response(
                {"detail": "Заказчик не может создавать кейс."},
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Получение списка проектов",
        description=(
            "Возвращает список всех проектов, упорядоченных по дате создания "
            "и другим параметрам. Позволяет пользователям просматривать "
            "проекты и искать их по различным критериям фильтрации."
        )
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Получение деталей проекта по ID",
        description=(
            "Возвращает детали конкретного проекта по его ID. "
            "Эта операция позволяет изучать полную информацию о проекте, "
            "включая описание, автора и статус."
        )
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Удаление кейса.",
        description="Удаляет кейс.",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Кейс успешно удален"
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Неавторизованный доступ"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="Доступ запрещен"
            ),
        }
    )
    def destroy(self, request, *args, **kwargs):
        case = self.get_object()

        if request.user != case.author:
            return Response(
                {"detail": "Только автор может удалить кейс."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().destroy(request, *args, **kwargs)

    # @action(
    #     detail=True,
    #     methods=['POST', 'DELETE'],
    # )
    # def favorite(self, request, pk):
    #     case_obj = get_object_or_404(Case, pk=pk)
    #     if request.method == 'POST':
    #         already_existed, created = FavoriteCase.objects.get_or_create(
    #             user=request.user,
    #             case=case_obj
    #         )
    #         if not created:
    #             return Response(
    #                 {'errors': 'Ошибка при создании записи'},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )
    #         serializer = CaseShortSerializer(case_obj,
    #                                          context={'request': request})
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     if request.method == 'DELETE':
    #         favorite = FavoriteCase.objects.filter(user=request.user,
    #                                                case=case_obj)
    #         if favorite.delete()[0]:
    #             return Response(
    #                 {'message': 'Проект удален из избранного.'},
    #                 status=status.HTTP_204_NO_CONTENT,
    #             )
    #         return Response(
    #             {'errors': 'Проект не найден в избранном.'},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
