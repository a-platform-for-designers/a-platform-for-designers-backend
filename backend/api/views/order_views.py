from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from api.permissions import IsAuthorOrReadOnly
from api.serializers.order_serializers import OrderReadSerializer, OrderWriteSerializer
from job.models import Order, FavoriteOrder


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderReadSerializer
        return OrderWriteSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def add_to(self, model, user, pk):
        order = get_object_or_404(Order, id=pk)
        model.objects.create(user=user, order=order)
        serializer = OrderReadSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        obj = model.objects.filter(user=user, order__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Этого заказа не существует'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['post', 'delete'])
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_to(FavoriteOrder, request.user, pk)
        return self.delete_from(FavoriteOrder, request.user, pk)
    