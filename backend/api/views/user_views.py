from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet as DjoserUserViewSet
from djoser.views import TokenCreateView as DjoserTokenCreateView
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from users.models import Subscription
from api.filters import DesignersFilter
from api.pagination import LimitPageNumberPagination
from api.serializers.empty_serializers import EmptySerializer
from api.serializers.subscription_serializers import (
    SubscriptionSerializer, SubscriptionCreateSerializer
)
from api.serializers.mentoring_serializers import MentorSerializer
from api.serializers.user_serializers import (
    AuthorListSerializer, UserProfileSerializer,
    ProfileCustomerSerializer, ProfileDesignerCreateSerializer,
    TokenResponseSerializer, UserProfileCreateSerializer
)
from api.permissions import IsAuthorOrReadOnly
# from api.mixins import RetrieveMixin


User = get_user_model()


@extend_schema(
    summary="Создание токена аутентификации",
    description="Создает и возвращает токен аутентификации для пользователя. "
    "Требуется предоставление корректных учетных данных пользователя. "
    "При успешной аутентификации возвращается токен, который должен "
    "использоваться для аутентификации в последующих запросах.",
    responses={
        200: TokenResponseSerializer(many=False),
        401: OpenApiResponse(
            description="Неавторизованный доступ или неверные учетные данные"
        )
    }
)
class TokenCreateView(DjoserTokenCreateView):
    pass


class ProfileCustomerViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    Создает профиль заказчика для пользователя.

    Пользователь должен иметь статус заказчика, чтобы создать профиль.
    В случае, если пользователь не имеет статуса заказчика, будет возвращен
    статус ошибки 403.

    """
    serializer_class = ProfileCustomerSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    @extend_schema(
        summary="Создание профиля заказчика",
        description="Метод для создания профиля заказчика. "
        "Требует статуса заказчика от пользователя.",
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=ProfileCustomerSerializer,
                description="Профиль успешно создан"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="Вы не являетесь заказчиком"
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Неавторизованный доступ"
            )
        }
    )
    def create(self, request, *args, **kwargs):
        if not request.user.is_customer:
            return Response({"detail": "Вы не являетесь заказчиком"},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileDesignerViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    Создает профиль дизайнера для пользователя.

    Пользователь должен иметь статус дизайнера,
    чтобы создать профиль дизайнера.
    В случае, если пользователь не является дизайнером,
    будет возвращен статус ошибки 403.

    """
    serializer_class = ProfileDesignerCreateSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    @extend_schema(
        summary="Создание профиля дизайнера",
        description="Метод для создания профиля дизайнера. "
        "Требует статуса дизайнера от пользователя.",
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=ProfileDesignerCreateSerializer,
                description="Профиль дизайнера успешно создан"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="Вы не являетесь дизайнером."
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Неавторизованный доступ"
            )
        }
    )
    def create(self, request, *args, **kwargs):
        if request.user.is_customer:
            return Response({"detail": "Вы не являетесь дизайнером."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с профилями пользователей.

    Операции:
    - POST: Создание нового пользователя.
    - GET (список): Получение списка пользователей.
    - GET (по ID): Получение информации о конкретном пользователе по ID.

    Фильтрация:
    - Специализация: Фильтруйте пользователей по их специализации.
    - Статус работы: Ищите пользователей в зависимости от их
    текущего статуса работы.
    - Навыки: Выбирайте пользователей на основе конкретных навыков.
    - Инструменты: Найдите пользователей, использующих
    определенные инструменты.

    Разрешения:
    - Создание профиля открыто для всех.
    - Операции чтения требуют аутентификации.

    """
    http_method_names = ['get', 'post', 'delete', 'head', 'options', 'trace']
    permission_classes = (AllowAny,)
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DesignersFilter

    def get_queryset(self):
        # Начальный набор данных
        queryset = User.objects.all()

        if self.action == 'list':
            # Фильтрация по количеству кейсов
            queryset = queryset.annotate(
                num_cases=Count('case')
            ).filter(
                num_cases__gte=1,
                is_customer=False
            )
            if self.request.user.is_authenticated:
                queryset = queryset.exclude(pk=self.request.user.pk)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return AuthorListSerializer
        elif self.action == 'create':
            return UserProfileCreateSerializer
        return UserProfileSerializer

    @extend_schema(
        summary="Создание нового пользователя",
        description="Регистрация и создание профиля нового "
        "пользователя в системе.",
        request=UserProfileCreateSerializer,
        responses={
            201: OpenApiResponse(
                response=UserProfileSerializer,
                description="Успешное создание пользователя."
            ),
            400: OpenApiResponse(
                description="Неверный запрос или ошибка в данных."
            )
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Получение списка пользователей",
        description="Получение списка всех пользователей "
        "с возможностью фильтрации.",
        responses={
            200: OpenApiResponse(
                response=AuthorListSerializer(many=True),
                description="Список пользователей предоставлен."
            )
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Получение информации о конкретном пользователе",
        description="Получение детальной информации о пользователе по ID.",
        responses={
            200: OpenApiResponse(
                response=UserProfileSerializer,
                description="Информация о пользователе предоставлена."
            ),
            404: OpenApiResponse(
                description="Пользователь не найден."
            )
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Получение профиля текущего пользователя",
        description="Возвращает профиль текущего пользователя или "
        "сообщение об ошибке, если пользователь не аутентифицирован.",
        responses={
            200: UserProfileSerializer,
            401: {"detail": "Вы не авторизованы."}
        }
    )
    @action(
        detail=False, methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        else:
            return Response(
                {"detail": "Вы не авторизованы."},
                status=status.HTTP_401_UNAUTHORIZED
            )

    @extend_schema(
        summary="Удаление пользователя",
        description="Удаление профиля пользователя из системы. "
        "Пользователь может удалить только свой профиль.",
        responses={
            204: OpenApiResponse(description="Пользователь успешно удален."),
            401: OpenApiResponse(description="Неавторизованный доступ."),
            403: OpenApiResponse(
                description="Запрещено. Нельзя удалять чужой профиль."
            ),
            404: OpenApiResponse(description="Пользователь не найден.")
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:

            user = self.get_object()

            if request.user == user:

                self.perform_destroy(user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:

                return Response(
                    {"detail": "Вы не можете удалить другого пользователя."},
                    status=status.HTTP_403_FORBIDDEN
                )

        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        summary="Управление подпиской",
        description="Позволяет пользователю подписаться на "
        "другого пользователя или отписаться от него.",
        methods=['POST', 'DELETE'],
        request=EmptySerializer,
    )
    @action(detail=True, methods=[
        'post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        current_user = request.user
        target_author_id = kwargs.get('pk')

        if request.method == 'POST':
            return self.manage_subscription(
                request,
                current_user,
                target_author_id,
                action_type='create'
            )

        elif request.method == 'DELETE':
            return self.manage_subscription(
                request,
                current_user,
                target_author_id,
                action_type='delete'
            )

    def manage_subscription(
        self,
        request,
        current_user,
        target_author_id,
        action_type
    ):
        # Получаем целевого автора из ID
        target_author = get_object_or_404(User, pk=target_author_id)

        if action_type == 'create':
            # Подготавливаем данные для сериализатора
            data = {'user': current_user.id, 'author': target_author.id}

            # Инициализируем сериализатор с данными
            serializer = SubscriptionCreateSerializer(data=data)

            # Проверяем валидность данных
            if serializer.is_valid():
                # Если данные валидны, сохраняем объект подписки
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                # Возвращаем ошибки валидации
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        elif action_type == 'delete':
            # Пытаемся получить инстанс подписки и удалить его
            try:
                subscription_instance = Subscription.objects.get(
                    user=current_user,
                    author=target_author
                )
                subscription_instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Subscription.DoesNotExist:
                # Если подписка не найдена, возвращаем ошибку 404
                return Response(
                    {"error": "Подписка не найдена."},
                    status=status.HTTP_404_NOT_FOUND
                )

    @extend_schema(
        summary='Список подписок пользователя',
        description=(
            "Возвращает список пользователей, на которых подписан текущий "
            "пользователь, позволяя управлять своими подписками."
        )
    )
    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        current_user = request.user
        queryset = User.objects.filter(subscribing__user=current_user)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            paginated_queryset,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class MentorViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Представление для получения списка менторов.

    Предоставляет список всех пользователей, классифицированных как менторы,
    с возможностью фильтрации по специализации, статусу работы,
    навыкам и инструментам. Это позволяет пользователям находить менторов,
    соответствующих конкретным критериям поиска.

    Операции:
    - GET: Получение списка менторов. Поддерживает фильтрацию и пагинацию
    для удобства просмотра и поиска менторов.

    Фильтрация:
    - Специализация: Фильтруйте менторов по их специализации.
    - Статус работы: Ищите менторов в зависимости от их
    текущего статуса работы.
    - Навыки: Выбирайте менторов на основе конкретных навыков.
    - Инструменты: Найдите менторов, использующих определенные инструменты.

    Пагинация:
    - Список менторов представлен с пагинацией, обеспечивая удобное
    пролистывание и просмотр большого количества профилей.

    Разрешения:
    - Доступ к списку менторов открыт для всех пользователей (AllowAny).

    """
    permission_classes = (AllowAny,)
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DesignersFilter
    queryset = User.objects.filter(
        profiledesigner__specialization__name='Менторство'
    ).distinct()
    serializer_class = MentorSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=MentorSerializer,
                description="Список менторов"
            ),
        },
        summary="Получение списка менторов",
        description="Получите детализированный список менторов."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CustomUserViewSet(DjoserUserViewSet):
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
