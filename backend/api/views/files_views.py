import mimetypes
import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from api.serializers.file_serializers import FileSerializer
from job.models import Chat


MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = [ext for ext, mime in mimetypes.types_map.items()]


class FileViewSet(viewsets.ModelViewSet):
    """
    Вью для загрузки файлов для отправки в сообщениях в чатах.

    Доступно только для аутентифицированных пользователей и поддерживает
    только загрузку файлов.
    (HTTP метод POST). Загружает файл в /media/messages/ и выдает
    ссылку для последующей отправки в сообщениях.

    """
    serializer_class = FileSerializer
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Загрузка файла",
        description="Загружает файл в /media/messages/ и выдает "
        "ссылку на него для последующей отправки в сообщениях.",
        responses={
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="Неавторизованный доступ"
            )
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        chat_id = self.request.data.get('chat')
        chat = get_object_or_404(Chat.objects.filter(pk=chat_id))
        file = self.request.data.get('file')
        try:
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension not in ALLOWED_EXTENSIONS:
                raise APIException('Недопустимый формат файла')

            if isinstance(file, bytes):
                content_file = ContentFile(file)
            else:
                content = file.read()
                content_file = ContentFile(content)

            if content_file.size > MAX_FILE_SIZE:
                raise APIException('Слишком большой размер файла')

            file_path = default_storage.save(
                'messages/' + file.name,
                content_file
            )
            serializer.save(
                sender=self.request.user,
                chat=chat,
                file=file_path
            )
        except (AttributeError, IOError):
            raise APIException('Неверный формат файла')
