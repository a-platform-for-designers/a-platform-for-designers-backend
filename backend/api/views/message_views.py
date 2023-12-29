from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from api.serializers.message_serializers import MessageSerializer
from job.models import Chat
from users.models import User


class MessageViewSet(viewsets.ModelViewSet):
    """
    Класс MessageViewSet для отправки сообщений.

    """

    serializer_class = MessageSerializer
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

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
        file = self.request.data.get('file')
        if file:
            try:
                if isinstance(file, bytes):
                    content_file = ContentFile(file)
                else:
                    content = file.read()
                    content_file = ContentFile(content)
                if content_file.size > settings.MAX_FILE_SIZE:
                    raise APIException('Слишком большой размер файла')
                file_path = default_storage.save(
                    'messages/' + file.name,
                    content_file
                )
                serializer.save(
                    sender=self.request.user,
                    chat=self.get_chat(),
                    file=file_path
                )
            except AttributeError:
                raise APIException('Неверный формат файла')
        else:
            serializer.save(
                sender=self.request.user,
                chat=self.get_chat()
            )
