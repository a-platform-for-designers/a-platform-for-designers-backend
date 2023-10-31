from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsInitiatorOrReceiverChatPermission
from api.serializers.chat_serializers import ChatCreateSerializer, ChatReadSerializer
from job.models import Chat


class ChatViewSet(viewsets.ModelViewSet):
    """"Класс ChatViewSet для работы с чатами."""

    http_method_names = ['get', 'post']
    permission_classes = [
        IsAuthenticated,
        IsInitiatorOrReceiverChatPermission
    ]

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(Q(initiator=user) | Q(receiver=user))

    def get_serializer_class(self):
        if self.request.method in ('POST'):
            return ChatCreateSerializer
        return ChatReadSerializer

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)
