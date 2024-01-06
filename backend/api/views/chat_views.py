import datetime

from django.http import Http404
from django.db.models import Q, Max
from django.db.models.functions import Coalesce
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.utils import OpenApiParameter

from api.pagination import LimitPageNumberPagination
from api.permissions import IsInitiatorOrReceiverChatPermission
from api.serializers.chat_serializers import ChatCreateSerializer
from api.serializers.chat_serializers import ChatReadSerializer
from job.models import Chat


@extend_schema(
    # ... другие параметры extend_schema ...
    parameters=[
        OpenApiParameter(
            name='id',
            description='ID чата',
            required=True,
            type=int
        ),
        # Добавьте другие параметры здесь, если они есть
    ]
)
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
                    "упорядоченных по дате последнего сообщения.",
        parameters=[
            OpenApiParameter(
                name='id',
                description='ID чата',
                required=True, type=int
            )
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Список чатов успешно получен"
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Неавторизованный доступ"
            ),
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создание чата",
        description="Создает новый чат с указанным пользователем.",
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description="Чат успешно создан"
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Неавторизованный доступ"
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Получение деталей чата по ID",
        description="Возвращает детали конкретного чата по его ID.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Детали чата успешно получены"
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Неавторизованный доступ"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="Доступ запрещен"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Чат не найден"
            ),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            chat = self.get_object()
        except Http404:
            # Возвращает 404 ошибку, если чат не найден
            return Response(
                {"detail": "Чат не найден."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверка, участник ли пользователь в чате
        if request.user != chat.initiator and request.user != chat.receiver:
            return Response(
                {"detail": "Вы не можете просматривать детали этого чата."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Если пользователь участник, вернуть детали чата
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
