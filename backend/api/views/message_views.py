from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsInitiatorOrReceiverMessagePermission
from api.serializers.message_serializers import MessageSerializer
from job.models import Chat


class MessageViewSet(viewsets.ModelViewSet):
    """"
    Класс MessageViewSet для работы с сообщениями чатов.

    """

    serializer_class = MessageSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [
        IsAuthenticated,
        IsInitiatorOrReceiverMessagePermission
    ]

    def get_chat(self):
        user = self.request.user
        return get_object_or_404(
            Chat.objects.filter(Q(initiator=user) | Q(receiver=user)),
            pk=self.kwargs.get('chat_id'),
        )

    def get_queryset(self):
        return self.get_chat().messages.all()

    def perform_create(self, serializer):
        serializer.save(
            sender=self.request.user,
            chat=self.get_chat()
        )
