import base64
import time

from django.core.files.base import ContentFile
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.serializers.message_serializers import MessageSerializer
from job.models import Chat
from users.models import User


class MessageViewSet(viewsets.ModelViewSet):
    """
    Вью для создания сообщений в чате.

    Доступно только для аутентифицированных пользователей и поддерживает
    только отправку сообщений.
    (HTTP метод POST). Обрабатывает создание чата между
    отправителем и получателем, если он еще не существует,
    и поддерживает отправку текстовых сообщений и файлов.

    """
    serializer_class = MessageSerializer
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=MessageSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=MessageSerializer,
                description="Сообщение успешно создано"
            ),
        },
        summary="Создание сообщения в чате",
        description="Позволяет аутентифицированным пользователям отправлять "
        "текстовые сообщения и файлы в чат."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_chat(self):
        user = self.request.user
        receiver_id = self.request.data.get('receiver')
        chat = Chat.objects.filter(
            Q(initiator__id=user.id, receiver__id=receiver_id)
            | Q(initiator__id=receiver_id, receiver__id=user.id)
        ).first()
        if not chat:
            chat = Chat.objects.create(
                initiator=user,
                receiver=get_object_or_404(
                    User.objects.filter(pk=receiver_id)
                )
            )
        return chat

    def perform_create(self, serializer):
        file_data = self.request.data.get('file')
        if file_data:
            file_format, file_data = file_data.split(';base64,')
            file_extension = file_format.split('/')[-1]
            if (
                file_extension == ('vnd.openxmlformats-officedocument.'
                                   'wordprocessingml.document')
                or file_extension == 'msword'
            ):
                file_extension = 'docx'
            filename = (f"{self.request.user.last_name}_"
                        f"{time.time()}.{file_extension}")
            file = ContentFile(
                base64.b64decode(file_data),
                name=filename
            )
            serializer.save(
                sender=self.request.user,
                chat=self.get_chat(),
                file=file
            )
        else:
            serializer.save(
                sender=self.request.user,
                chat=self.get_chat()
            )
