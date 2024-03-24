from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.filters import CaseFilter
from api.pagination import LimitPageNumberPagination
from api.serializers.case_serializers import (
    CaseSerializer, CaseCreateSerializer,
    CaseFavoriteShortSerializer
)
from api.serializers.empty_serializers import EmptySerializer
from job.models import Case, FavoriteCase, Like
from api.permissions import IsAuthorOrReadOnly


class CaseViewSet(ModelViewSet):
    """
    Вью для работы с проектами авторов.

    list/retrieve:
    Возвращает список всех кейсов, упорядоченных
    по дате создания и другим параметрам.
    Также позволяет получать кейс по ID.

    """
    http_method_names = ['get', 'post', 'delete', 'patch']
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

    @extend_schema(
        request=EmptySerializer,
        summary="Переключение состояния избранного для проекта",
        description="Добавляет проект в избранные пользователя или "
        "удаляет его оттуда, если он уже добавлен.",
        responses={
            200: "Проект удален из избранного",
            201: "Проект добавлен в избранное"
        }
    )
    @action(
        detail=True, methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def favorite_case(self, request, pk=None):
        user = request.user
        case = self.get_object()
        favorite_exists = FavoriteCase.objects.filter(
            user=user, case=case
        ).exists()

        if favorite_exists:
            FavoriteCase.objects.filter(user=user, case=case).delete()
            return Response(
                {"detail": "Проект удален из избранного"},
                status=status.HTTP_200_OK
            )
        else:
            FavoriteCase.objects.create(user=user, case=case)
            return Response(
                {"detail": "Проект добавлен в избранное"},
                status=status.HTTP_201_CREATED
            )

    @extend_schema(
        request=EmptySerializer,
        summary='Лайк кейсу',
        description=(
            "Текущий пользователь ставит лайк кейсу. Если лайк уже стоит, он "
            "будет удален. Возвращает сообщение о создании/удалении лайка."
        ),
        responses={
            200: OpenApiResponse(description="Лайк удален"),
            201: OpenApiResponse(description="Лайк поставлен"),
        }
    )
    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,)
    )
    def like(self, request, pk):
        user = request.user
        case = get_object_or_404(Case, pk=pk)
        like = case.case_likes.filter(liker=user).exists()
        if like:
            case.case_likes.get(liker=user).delete()
            return Response(
                {"detail": "Лайк удален"},
                status=status.HTTP_200_OK
            )
        else:
            Like.objects.create(liker=user, case=case)
            return Response(
                {"detail": "Лайк поставлен"},
                status=status.HTTP_201_CREATED
            )


@extend_schema(
    summary="Получение списка избранных проектов",
    description=(
        "Возвращает список всех проектов (cases), добавленных в избранное "
        "текущим пользователем. Предоставляет подробную информацию по каждому "
        "проекту, включая статус избранного."
    ),
    responses={200: CaseSerializer(many=True)}
)
class FavoriteCasesView(APIView):
    """
    Список избранных проектов пользователя.

    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorite_cases = FavoriteCase.objects.filter(user=request.user)
        cases = [fav_case.case for fav_case in favorite_cases]
        serializer = CaseFavoriteShortSerializer(
            cases, many=True, context={'request': request}
        )
        return Response(serializer.data)
