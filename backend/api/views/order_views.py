from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.filters import OrdersFilter
from api.pagination import LimitPageNumberPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers.order_serializers import (
    OrderReadSerializer, OrderAuthorReadSerializer, OrderWriteSerializer,
    OrderResponseSerializer,
    OrderAuthorListReadSerializer

)
from job.models import Order, OrderResponse
# from users.models import User
# FavoriteOrderSerializer, FavoriteOrder,


class OrderViewSet(viewsets.ModelViewSet):
    """
    Для управления заказами. Поддерживает операции создания, чтения,
    обновления и удаления заказов,
    а также включает специализированные действия для управления публикацией
    и откликами на заказы.

    Основные методы:
    - list: Возвращает список всех опубликованных заказов.
    - create: Позволяет заказчикам создавать новые заказы.
    - retrieve: Возвращает детали конкретного заказа.
    - destroy: Удаляет заказ.

    Специализированные действия:
    - respond: Позволяет исполнителям откликаться на заказы
    или отзывать свои отклики.
    - publish: Позволяет заказчикам публиковать или снимать
    с публикации свои заказы.
    - my_orders: Возвращает заказы текущего пользователя,
    различая заказчиков и исполнителей.

    Фильтрация, пагинация и разрешения:
    - Поддерживает фильтрацию заказов.
    - Не использует пагинацию.
    - Различные классы разрешений применяются в зависимости от действия
    и роли пользователя.

    """
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = LimitPageNumberPagination
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrdersFilter

    def get_queryset(self):
        base_queryset = Order.objects.all()
        if self.action == 'list':
            return base_queryset.filter(is_published=True)
        return base_queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderReadSerializer
        elif self.action == 'retrieve':
            order = self.get_object()
            if self.request.user == order.customer:
                return OrderAuthorReadSerializer
            return OrderReadSerializer
        elif self.action in ('create', 'partial_update'):
            return OrderWriteSerializer

    @extend_schema(
        summary="Список заказов",
        description="Возвращает список всех опубликованных заказов."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создание заказа",
        description="Позволяет заказчикам создавать новые заказы.",
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description="Заказ успешно создан"
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Неавторизованный доступ"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="Создавать заказы могут только заказчики"
            )
        }
    )
    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Неавторизованный доступ"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        elif request.user.is_customer:
            return super().create(request, *args, **kwargs)
        else:
            return Response(
                {"detail": "Создавать заказы могут только заказчики"},
                status=status.HTTP_403_FORBIDDEN
            )

    @extend_schema(
        summary="Получение деталей заказа",
        description="Возвращает детали конкретного заказа.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Детали заказа предоставлены"
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Неавторизованный доступ"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Заказ не найден"
            )
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @extend_schema(
        summary="Удаление заказа",
        description="Удаляет заказ.",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Заказ успешно удален"
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Неавторизованный доступ"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="У вас нет доступа удалять этот заказ"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Заказ не найден"
            )
        }
    )
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Неавторизованный доступ"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        order = get_object_or_404(Order, id=kwargs.get('pk'))
        if request.user != order.customer:
            return Response(
                {"detail": "У вас нет доступа удалять этот заказ"},
                status=status.HTTP_403_FORBIDDEN
            )

        return self.delete_object(Order, request.user, kwargs.get('pk'))

    @staticmethod
    def delete_object(model, user, pk):
        obj = model.objects.filter(user=user, order__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"errors": "Заказ уже удален или не существует."},
                status=status.HTTP_404_NOT_FOUND
            )

    @staticmethod
    def create_object(serializer, pk, request):
        order = get_object_or_404(Order, id=pk)
        data = {
            'user': request.user.id,
            'order': order.id
        }
        serializer = serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # @action(
    #     detail=True,
    #     methods=['post', 'delete'],
    #     permission_classes=[IsAuthenticated]
    # )
    # def favorite(self, request, pk):
    #     if request.method == 'POST':
    #         return self.create_object(FavoriteOrderSerializer, pk, request)
    #     return self.delete_object(FavoriteOrder, request.user, pk)

    @extend_schema(
        summary="Отклик на заказ",
        description="Позволяет дизайнерам откликаться на заказы "
                    "и удалять свои отклики. "
                    "DELETE запрос используется для отмены уже "
                    "существующего отклика, "
                    "что удаляет дизайнера из списка потенциальных "
                    "исполнителей заказа.",
        methods=['post', 'delete'],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Отклик успешно создан или удален"
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Неавторизованный доступ"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="Доступ запрещен"
            )
        }
    )
    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def respond(self, request, pk):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Неавторизованный доступ"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if request.method == 'POST':
            if self.request.user.is_customer:
                return Response(
                    {'errors': 'Заказчик не может откликаться на вакансии'},
                    status=status.HTTP_403_FORBIDDEN
                )
            return self.create_object(OrderResponseSerializer, pk, request)
        return self.delete_object(OrderResponse, request.user, pk)

    @extend_schema(
        summary="Публикация заказа",
        description="Позволяет публиковать/снимать с публикации свои заказы.",
        methods=['patch'],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Заказ успешно опубликован или снят с публикации"
            ),
            status.HTTP_201_CREATED: OpenApiResponse(
                description="Заказ успешно снят с публикации"
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Неавторизованный доступ"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="У вас нет доступа корректировать заказ"
            )
        }
    )
    @action(
        detail=True,
        methods=['patch'],
        permission_classes=[IsAuthenticated]
    )
    def publish(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        if self.request.user != order.customer:
            return Response(
                {'errors': 'У вас нет доступа корректировать заказ'},
                status=status.HTTP_403_FORBIDDEN
            )
        if order.is_published:
            order.is_published = False
            order.save()
            return Response(
                {'message': 'Заказ успешно снят с публикации'},
                status=status.HTTP_201_CREATED
            )
        order.is_published = True
        order.save()
        return Response(
            {'message': 'Заказ успешно опубликован'},
            status=status.HTTP_200_OK
        )

    @extend_schema(
        summary="Заказы пользователя",
        description="Возвращает заказы пользователя.",
        methods=['get'],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Заказы пользователя успешно получены"
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Неавторизованный доступ"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="Доступ запрещен"
            )
        }
    )
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def my_orders(self, request):
        user = self.request.user

        if not user.is_authenticated:
            return Response(
                {"detail": "Неавторизованный доступ"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user.is_customer:
            orders = user.orders.all()
            serializer = OrderAuthorListReadSerializer(orders, many=True)
            return Response(serializer.data)

        responses = user.order_responses.values_list('order', flat=True)
        orders = Order.objects.filter(id__in=responses)
        serializer = OrderReadSerializer(orders, many=True)
        return Response(serializer.data)

    # @action(
    #     detail=True,
    #     methods=['patch'],
    #     url_path=r'approve_customer/(?P<designer_id>\d+)'
    # )
    # def approve_customer(self, request, pk, designer_id):
    #     order = get_object_or_404(Order, id=pk)
    #     if self.request.user != order.customer:
    #         return Response(
    #             {'errors': 'Только автор заказа может назначать исполнит'},
    #             status=status.HTTP_403_FORBIDDEN
    #         )
    #     if order.executor is not None:
    #         return Response(
    #             {'errors': 'У заказа уже есть исполнитель'},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     try:
    #         response = OrderResponse.objects.get(
    #             user=designer_id,
    #             order=order.id
    #         )
    #         order.executor = response.user
    #         order.save()
    #         return Response(
    #             {'message': 'Исполнитель успешно добавлен'},
    #             status=status.HTTP_201_CREATED
    #         )
    #     except OrderResponse.DoesNotExist:
    #         return Response(
    #             {'message': 'Данный пользователь не откликался на заказ'},
    #             status=status.HTTP_400_HTTP_400_BAD_REQUEST
    #         )

    # @action(detail=True, methods=['patch'])
    # def delete_customer(self, request, pk):
    #     order = get_object_or_404(Order, id=pk)
    #     if self.request.user != order.customer:
    #         return Response(
    #             {'errors': 'Только автор заказа может удалять исполнителей'},
    #             status=status.HTTP_403_FORBIDDEN
    #         )
    #     if order.executor is None:
    #         return Response(
    #             {'errors': 'У заказа нет исполнителя'},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     order.executor = None
    #     order.save()
    #     return Response(
    #         {'message': 'Исполнитель успешно удален'},
    #         status=status.HTTP_201_CREATED
    #     )
