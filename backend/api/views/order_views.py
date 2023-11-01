from rest_framework import viewsets

from api.permissions import IsAuthorOrReadOnly
from api.serializers.order_serializers import OrderSerializer
from job.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
