from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.pagination import LimitPageNumberPagination
from job.models import CaseImage, Comment, Sphere
from users.models import Subscription
from .serializers import (CaseImageSerializer, CommentSerializer,
                          SphereSerializer, )
from api.serializers.subscription_serializers import SubscriptionSerializer
from api.serializers.user_serializers import UserProfileSerializer
from api.serializers.user_serializers import ProfileCustomerSerializer
from api.serializers.user_serializers import ProfileDesignerSerializer
from api.permissions import IsOwnerOrReadOnly
from users.models import ProfileCustomer, ProfileDesigner
from job.models import Case, Favorite, Instrument, Skill
from pagination import LimitPageNumberPagination
from serializers import (CaseSerializer,
                         CaseCreateSerializer,
                         CaseShortSerializer,
                         InstrumentSerializer,
                         SkillSerializer)


User = get_user_model()


class ProfileCustomerViewSet(viewsets.ModelViewSet):
    queryset = ProfileCustomer.objects.all().order_by('id')
    serializer_class = ProfileCustomerSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        if not request.user.is_customer:
            return Response({"detail": "Вы не являетесь покупателем."},
                            status=status.HTTP_403_FORBIDDEN)
        if (
            not request.user.is_staff and
            request.user.id != request.data.get('user')
        ):
            return Response({"detail": "Нет разрешения."},
                            status=status.HTTP_403_FORBIDDEN)
        if ProfileCustomer.objects.filter(user=request.user).exists():
            return Response({"detail": "Профиль уже существует."},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


class ProfileDesignerViewSet(viewsets.ModelViewSet):
    queryset = ProfileDesigner.objects.all().order_by('id')
    serializer_class = ProfileDesignerSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        if request.user.is_customer:
            return Response({"detail": "Вы не являетесь дизайнером."},
                            status=status.HTTP_403_FORBIDDEN)
        if (
            not request.user.is_staff and
            request.user.id != request.data.get('user')
        ):
            return Response({"detail": "У вас нет разрешения."},
                            status=status.HTTP_403_FORBIDDEN)
        if ProfileDesigner.objects.filter(user=request.user).exists():
            return Response({"detail": "Профиль уже существует."},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


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

    queryset = User.objects.select_related(
        'profilecustomer',
        'profiledesigner'
    ).order_by('id')
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


class InstrumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    pagination_class = None
    permission_classes = [AllowAny, ]
    search_fields = ['^name', ]


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    pagination_class = None
    permission_classes = [AllowAny, ]


class CaseViewSet(ModelViewSet):
    """"
    Класс CaseViewSet для работы с проектами авторов.

    """
    queryset = Case.objects.all()
    pagination_class = LimitPageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CaseSerializer
        return CaseCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
    )
    def favorite(self, request, pk):
        case_obj = get_object_or_404(Case, pk=pk)
        if request.method == 'POST':
            already_existed, created = Favorite.objects.get_or_create(
                user=request.user,
                case=case_obj
            )
            if not created:
                return Response(
                    {'errors': 'Ошибка при создании записи.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = CaseShortSerializer(case_obj,
                                             context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            favorite = request.user.favorites.all()
            if favorite:
                favorite.delete()
                return Response(
                    {'message': 'Проект удален из избранного.'},
                    status=status.HTTP_204_NO_CONTENT,
                )
            return Response(
                {'errors': 'Проект не найден в избранном.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
