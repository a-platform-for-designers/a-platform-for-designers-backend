from django.db.models import Q, Max
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.pagination import LimitPageNumberPagination
from api.permissions import IsInitiatorOrReceiverChatPermission
from api.serializers.chat_serializers import ChatCreateSerializer
from api.serializers.chat_serializers import ChatReadSerializer
from job.models import Chat


class ChatViewSet(viewsets.ModelViewSet):
    """"
    Класс ChatViewSet для работы с чатами.

    """

    http_method_names = ['get', 'post']
    permission_classes = [
        IsAuthenticated,
        IsInitiatorOrReceiverChatPermission
    ]
    pagination_class = LimitPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Chat.objects.filter(
            Q(initiator=user) | Q(receiver=user)
        ).annotate(
            last_message_date=Max('messages__pub_date')
        ).order_by('-last_message_date', '-id')
        return queryset

    def get_serializer_class(self):
        if self.request.method in ('POST',):
            return ChatCreateSerializer
        return ChatReadSerializer

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)
