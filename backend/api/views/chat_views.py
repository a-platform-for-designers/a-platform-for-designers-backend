import datetime

from django.db.models import Q, Max
from django.db.models.functions import Coalesce
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from api.pagination import LimitPageNumberPagination
from api.permissions import IsInitiatorOrReceiverChatPermission
from api.serializers.chat_serializers import ChatCreateSerializer
from api.serializers.chat_serializers import ChatReadSerializer
from job.models import Chat


class ChatViewSet(viewsets.ModelViewSet):
    """
    Вью для работы с чатами.
    Также позволяет получать чат по ID.

    """

    http_method_names = ['get', 'post']
    permission_classes = [
        IsAuthenticated,
        IsInitiatorOrReceiverChatPermission
    ]
    pagination_class = LimitPageNumberPagination

    @extend_schema(
        summary="Получение списка чатов",
        description="Возвращает список всех чатов для данного пользователя, "
                    "упорядоченных по дате последнего сообщения."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создание чата",
        description="Создает новый чат с указанным пользователем."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Получение деталей чата по ID",
        description="Возвращает детали конкретного чата по его ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        null_date = datetime.datetime.min
        queryset = Chat.objects.filter(
            Q(initiator=user) | Q(receiver=user)
        ).annotate(
            last_message_date=Coalesce(Max('messages__pub_date'), null_date)
        ).order_by('-last_message_date', '-id')
        return queryset

    def get_serializer_class(self):
        if self.request.method in ('POST',):
            return ChatCreateSerializer
        return ChatReadSerializer

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)
