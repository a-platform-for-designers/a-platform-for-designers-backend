from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.pagination import LimitPageNumberPagination
from job.models import CaseImage, Comment, Sphere
from users.models import Subscription

from .serializers import (CaseImageSerializer, CommentSerializer,
                          SphereSerializer, SubscriptionSerializer,
                          UserProfileSerializer, CaseImageShortSerializer)

User = get_user_model()

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

    """

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
            serializer = SubscriptionSerializer(
                target_author,
                data=request.data,
                context={"request": request}
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


class CaseImageViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post')
    queryset = CaseImage.objects.all()
    serializer_class = CaseImageSerializer

    @action(detail=True,
            methods=['get', ])
    def portfolio(self, request, pk):
        # забираем объекты обложки данного автора
        cover = CaseImage

        # serializer = CaseImageShortSerializer



class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post')
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class SphereViewSet(viewsets.ModelViewSet):
    http_method_names = ('get')
    queryset = Sphere.objects.all()
    serializer_class = SphereSerializer
