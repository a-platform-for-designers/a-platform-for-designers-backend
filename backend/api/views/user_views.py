from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet
from djoser.views import TokenCreateView as DjoserTokenCreateView
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from users.models import Subscription
from api.filters import DesignersFilter
from api.pagination import LimitPageNumberPagination
from api.serializers.subscription_serializers import (
    SubscriptionSerializer, SubscriptionCreateSerializer
)
from api.serializers.user_serializers import (
    AuthorListSerializer, UserProfileSerializer,
    ProfileCustomerSerializer, ProfileDesignerCreateSerializer,
    TokenResponseSerializer, UserProfileCreateSerializer,
)
from api.permissions import IsAuthorOrReadOnly


User = get_user_model()


@extend_schema(
    responses=TokenResponseSerializer(many=False)
)
class TokenCreateView(DjoserTokenCreateView):
    """
    Создает и возвращает токен аутентификации для пользователя.

    Требуется предоставление корректных учетных данных пользователя.
    При успешной аутентификации возвращается токен, который должен
    использоваться для аутентификации в последующих запросах.

    """
    pass


@extend_schema(
    tags=['profiles'],
    operation_id='create_customer_profile',
    summary='Создание профиля заказчика',
    description=(
        'Эндпоинт для создания профиля заказчика. '
        'Доступ ограничен для пользователей с ролью "заказчик".'
    ),
    responses={
        201: OpenApiResponse(
            description='Успешное создание профиля заказчика.'
        ),
        400: OpenApiResponse(
            description='Некорректный запрос или данные. '
            'Проверьте предоставленные данные.'
        ),
        403: OpenApiResponse(
            description='Доступ запрещен. '
            'Требуется статус заказчика для создания профиля.'
        )
    }
)
class ProfileCustomerViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    Создает профиль для пользователя с ролью заказчика.

    Пользователь должен иметь статус заказчика, чтобы создать профиль.
    В случае, если пользователь не имеет статуса заказчика, будет возвращен
    статус ошибки 403.

    """

    serializer_class = ProfileCustomerSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def create(self, request, *args, **kwargs):
        if not request.user.is_customer:
            return Response({"detail": "Вы не являетесь заказчиком"},
                            status=status.HTTP_403_FORBIDDEN)
        # if (
        #     not request.user.is_staff
        #     and request.user.id != request.data.get('user')
        # ):
        #     return Response({"detail": "Нет разрешения."},
        #                     status=status.HTTP_403_FORBIDDEN)
        # if ProfileCustomer.objects.filter(user=request.user).exists():
        #     return Response({"detail": "Профиль уже существует"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    tags=['profiles'],
    operation_id='create_designer_profile',
    summary='Создание профиля дизайнера',
    description='Эндпоинт для создания профиля дизайнера.',
    responses={
        201: OpenApiResponse(description='Профиль дизайнера успешно создан'),
        400: OpenApiResponse(description='Ошибка создания профиля'),
        403: OpenApiResponse(
            description='Доступ запрещен. Пользователь является заказчиком'
        ),
    }
)
class ProfileDesignerViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    Создает профиль для пользователя с ролью дизайнера.

    Пользователь не должен иметь статус заказчика,
    чтобы создать профиль дизайнера.
    В случае, если пользователь является заказчиком,
    будет возвращен статус ошибки 403.

    """
    serializer_class = ProfileDesignerCreateSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def create(self, request, *args, **kwargs):
        if request.user.is_customer:
            return Response({"detail": "Вы не являетесь дизайнером."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    tags=['user_profiles'],
    operation_id='list_user_profiles',
    summary='Список профилей пользователей',
    description=(
        'Получение списка профилей пользователей с возможностью фильтрации '
        'по параметрам, включая количество кейсов и статус работы.'
    ),
    responses={
        200: UserProfileSerializer(
            many=True,
            description='Список профилей пользователей успешно получен.'
        ),
        404: OpenApiResponse(description='Профили пользователей не найдены.')
    }
)
@extend_schema(
    methods=['create'],
    summary='Создание профиля пользователя',
    description=(
        'Эндпоинт для создания профиля пользователя. '
        'Доступен только для аутентифицированных пользователей.'
    ),
    responses={
        201: UserProfileSerializer(
            description='Профиль пользователя успешно создан.'
        ),
        400: OpenApiResponse(
            description='Ошибка в данных запроса. '
            'Невозможно создать профиль с предоставленными данными.'
        ),
        403: OpenApiResponse(
            description='Доступ запрещён. '
            'Требуется аутентификация пользователя.'
        )
    }
)
class UserProfileViewSet(UserViewSet):
    """
    Предоставляет операции для работы с профилями пользователей,
    включая создание, просмотр, обновление и удаление профилей.

    list:
    Возвращает список всех профилей пользователей с дополнительной информацией.

    create:
    Позволяет аутентифицированным пользователям создать
    новый профиль пользователя.

    """
    permission_classes = (AllowAny,)
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DesignersFilter

    def get_queryset(self):
        # Начальный набор данных
        queryset = User.objects.all()

        if self.action == 'list':
            # Фильтрация по количеству кейсов и статусу заказчика
            queryset = queryset.annotate(
                num_cases=Count('case')
            ).filter(
                num_cases__gte=1,
                is_customer=False
            )

            if self.request.user.is_authenticated:
                queryset = queryset.exclude(pk=self.request.user.pk)

            # Фильтрация по статусу работы дизайнера
            work_status = self.request.query_params.get('work_status')
            if work_status is not None:
                work_status = work_status.lower() in ['true', '1', 't']
                queryset = queryset.filter(
                    profiledesigner__work_status=work_status
                )
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return AuthorListSerializer
        elif self.action == 'create':
            return UserProfileCreateSerializer
        return UserProfileSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        current_user = request.user
        target_author_id = self.kwargs.get('id')
        target_author = get_object_or_404(User, id=target_author_id)

        if request.method == 'POST':
            return self.manage_subscription(
                request,
                current_user,
                target_author,
                action_type='create'
            )

        if request.method == 'DELETE':
            return self.manage_subscription(
                request,
                current_user,
                target_author,
                action_type='delete'
            )

    def manage_subscription(
            self,
            request,
            current_user,
            target_author,
            action_type
    ):
        if action_type == 'create':
            serializer = SubscriptionCreateSerializer(
                data={
                    'user': current_user.id,
                    'author': target_author.id
                },
            )
            serializer.is_valid(raise_exception=True)
            Subscription.objects.create(
                user=current_user,
                author=target_author
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif action_type == 'delete':
            subscription_instance = get_object_or_404(
                Subscription,
                user=current_user,
                author=target_author
            )
            subscription_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

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


class MentorViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """"
    Класс MentorViewSet включает в себя только list-метод
    для отображения дизайнеров-менторов.

    """
    permission_classes = (AllowAny,)
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DesignersFilter
    queryset = User.objects.filter(
        profiledesigner__specialization__name='Менторство'
    ).distinct()
    serializer_class = AuthorListSerializer
