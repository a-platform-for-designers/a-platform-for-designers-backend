from rest_framework import viewsets

from api.permissions import IsAuthorOrReadOnly
from api.serializers.order_serializers import OrderReadSerializer, OrderWriteSerializer
from job.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderReadSerializer
        return OrderWriteSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
