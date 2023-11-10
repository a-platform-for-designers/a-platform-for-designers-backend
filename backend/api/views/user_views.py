from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet
from djoser.views import TokenCreateView as DjoserTokenCreateView
from rest_framework import viewsets, status, mixins
# from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

# from users.models import Subscription
from api.pagination import LimitPageNumberPagination
# from api.serializers.subscription_serializers import (
#    SubscriptionSerializer, SubscriptionCreateSerializer
# )
from api.serializers.user_serializers import UserProfileSerializer
from api.serializers.user_serializers import UserProfileCreateSerializer
from api.serializers.user_serializers import UserProfileUpdateSerializer
from api.serializers.user_serializers import UserListSerializer
from api.serializers.user_serializers import ProfileCustomerSerializer
from api.serializers.user_serializers import ProfileDesignerSerializer
from api.serializers.user_serializers import TokenResponseSerializer
from api.permissions import IsOwnerOrReadOnly
from users.models import ProfileCustomer, ProfileDesigner


User = get_user_model()


@extend_schema(
    responses=TokenResponseSerializer(many=False)
)
class TokenCreateView(DjoserTokenCreateView):
    pass


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
        if ProfileDesigner.objects.filter(user=request.user).exists():
            return Response({"detail": "Профиль уже существует."},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserProfileViewSet(UserViewSet):
    """
    Класс UserProfileViewSet для работы с профилями пользователей.
    """

    queryset = User.objects.all()
    pagination_class = LimitPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'retrieve':
            return UserProfileSerializer
        elif self.action == 'partial_update':
            return UserProfileUpdateSerializer
        elif self.action == 'create':
            return UserProfileCreateSerializer
        else:
            return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'partial_update':
            self.permission_classes = [IsOwnerOrReadOnly, ]
        else:
            self.permission_classes = [AllowAny, ]
        return super(UserProfileViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()

    # @action(
    #     detail=True,
    #     methods=['post', 'delete'],
    #     permission_classes=[IsAuthenticated]
    # )
    # def subscribe(self, request, **kwargs):
    #     current_user = request.user
    #     target_author_id = self.kwargs.get('id')
    #     target_author = get_object_or_404(User, id=target_author_id)

    #     if request.method == 'POST':
    #         return self.manage_subscription(
    #             request,
    #             current_user,
    #             target_author,
    #             action_type='create'
    #         )

    #     if request.method == 'DELETE':
    #         return self.manage_subscription(
    #             request,
    #             current_user,
    #             target_author,
    #             action_type='delete'
    #         )

    # def manage_subscription(
    #         self,
    #         request,
    #         current_user,
    #         target_author,
    #         action_type
    # ):
    #     if action_type == 'create':
    #         serializer = SubscriptionCreateSerializer(
    #             data={
    #                 'user': current_user.id,
    #                 'author': target_author.id
    #             },
    #         )
    #         serializer.is_valid(raise_exception=True)
    #         Subscription.objects.create(
    #             user=current_user,
    #             author=target_author
    #         )
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     elif action_type == 'delete':
    #         subscription_instance = get_object_or_404(
    #             Subscription,
    #             user=current_user,
    #             author=target_author
    #         )
    #         subscription_instance.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(
    #     detail=False,
    #     permission_classes=[IsAuthenticated]
    # )
    # def subscriptions(self, request):
    #     current_user = request.user
    #     queryset = User.objects.filter(subscribing__user=current_user)
    #     paginated_queryset = self.paginate_queryset(queryset)
    #     serializer = SubscriptionSerializer(
    #         paginated_queryset,
    #         many=True,
    #         context={'request': request}
    #     )
    #     return self.get_paginated_response(serializer.data)

    # @action(
    #     detail=True,
    #     methods=['get']
    # )
    # def portfolio(self, request):
    #     pass
