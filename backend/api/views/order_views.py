from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from api.pagination import LimitPageNumberPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers.order_serializers import (
    OrderReadSerializer, OrderAuthorReadSerializer, OrderWriteSerializer,
    FavoriteOrderSerializer, OrderResponseSerializer

)
from job.models import FavoriteOrder, Order, OrderResponse
from users.models import User


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    pagination_class = LimitPageNumberPagination
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.action == 'list':
                return OrderReadSerializer
            elif self.action == 'retrieve':
                order = self.get_object()
                if self.request.user == order.customer:
                    return OrderAuthorReadSerializer
                return OrderReadSerializer
        return OrderWriteSerializer

    def create(self, request, *args, **kwargs):
        if request.user.is_customer:
            return super().create(request, *args, **kwargs)
        else:
            return Response(
                {"detail": "Создавать заказы могут только заказчики"},
                status=status.HTTP_403_FORBIDDEN
            )

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

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

    @staticmethod
    def delete_object(model, user, pk):
        obj = model.objects.filter(user=user, order__id=pk)
        if obj.delete()[0]:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Заказ уже удален!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.create_object(FavoriteOrderSerializer, pk, request)
        return self.delete_object(FavoriteOrder, request.user, pk)

    @action(detail=True, methods=['post', 'delete'])
    def respond(self, request, pk):
        if request.method == 'POST':
            if self.request.user.is_customer:
                return Response(
                    {'errors': 'Заказчик не может откликаться на вакансии'},
                    status=status.HTTP_403_FORBIDDEN
                )
            return self.create_object(OrderResponseSerializer, pk, request)
        return self.delete_object(OrderResponse, request.user, pk)

    @action(detail=True, methods=['patch'])
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
            {'message': 'Заказ успешно снят с публикации'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        user = self.request.user
        if user.is_customer:
            orders = user.orders.all()
            serializer = OrderReadSerializer(orders, many=True)
            return Response(serializer.data)
        responses = user.order_responses.values_list('order').all()
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
