from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import Subscription
from api.pagination import LimitPageNumberPagination
from api.serializers.subscription_serializers import (
    SubscriptionSerializer, SubscriptionCreateSerializer
)
from api.serializers.user_serializers import UserProfileSerializer
from api.serializers.user_serializers import ProfileCustomerSerializer
from api.serializers.user_serializers import ProfileDesignerSerializer
from api.permissions import IsOwnerOrReadOnly
from users.models import ProfileCustomer, ProfileDesigner


User = get_user_model()


class ProfileCustomerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = ProfileCustomer.objects.all().order_by('id')
    serializer_class = ProfileCustomerSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        if not request.user.is_customer:
            return Response({"detail": "Вы не являетесь заказчиком"},
                            status=status.HTTP_403_FORBIDDEN)
        if (
            not request.user.is_staff
            and request.user.id != request.data.get('user')
        ):
            return Response({"detail": "Нет разрешения."},
                            status=status.HTTP_403_FORBIDDEN)
        if ProfileCustomer.objects.filter(user=request.user).exists():
            return Response({"detail": "Профиль уже существует"},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileDesignerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = ProfileDesigner.objects.all().order_by('id')
    serializer_class = ProfileDesignerSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        if request.user.is_customer:
            return Response({"detail": "Вы не являетесь дизайнером."},
                            status=status.HTTP_403_FORBIDDEN)
        if (
            not request.user.is_staff
            and request.user.id != request.data.get('user')
        ):
            return Response({"detail": "У вас нет разрешения."},
                            status=status.HTTP_403_FORBIDDEN)
        if ProfileDesigner.objects.filter(user=request.user).exists():
            return Response({"detail": "Профиль уже существует."},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserProfileViewSet(UserViewSet):
    """"
    Класс UserProfileViewSet для работы с профилями пользователей.
    Добавляет дополнительные функции для управления подписками.

    Методы:
        subscribe: обрабатывает POST и DELETE запросы
        для создания и удаления подписок на авторов.
        manage_subscription: метод для создания и удаления подписок.
        subscriptions: возвращает список авторов,
        на которых подписан пользователь.

    Эндпоинты:
        POST /api/users/{id}/subscribe/
        DELETE /api/users/{id}/subscribe/
        GET /api/users/subscriptions/
    Внимание! Код картинки для регистрации пользователя через json:
    iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVQI12P4//8/AAX+Av7czFnnAAAAAElFTkSuQmCC
    """

    # queryset = User.objects.select_related(
    #     'profilecustomer',
    #     'profiledesigner',
    # ).order_by('id')
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitPageNumberPagination

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

    @action(
        detail=True,
        methods=['get']
    )
    def portfolio(self, request):
        pass
