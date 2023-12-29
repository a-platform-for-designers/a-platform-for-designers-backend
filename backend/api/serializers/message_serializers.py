import filetype

from rest_framework import serializers
from drf_extra_fields.fields import Base64FileField

from api.serializers.chat_serializers import ChatReadSerializer
from api.serializers.user_serializers import UserChatAndMessageSerializer
from job.models import Message


class MyCustomBase64FileField(Base64FileField):
    """
    Кастомный сериализатор для обработки файлов в base64 формате.

    """
    ALLOWED_MIME_TYPES = {
        'image/jpeg': 'jpg',
        'image/png': 'png',
        'application/pdf': 'pdf',
        ('application/vnd.openxmlformats-officedocument.'
         'wordprocessingml.document'): 'docx',
    }

    ALLOWED_TYPES = ['pdf', 'docx', 'doc', 'jpg', 'jpeg', 'png']

    def get_file_extension(self, filename, decoded_file):
        extension = filetype.guess_extension(decoded_file)
        if extension in self.ALLOWED_TYPES:
            return extension
        return None

    def to_internal_value(self, data):
        if isinstance(data, str):
            return super().to_internal_value(data)
        return data


class MessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор сообщения.

    """
    sender = UserChatAndMessageSerializer(read_only=True)
    chat = ChatReadSerializer(read_only=True)
    receiver = serializers.IntegerField(required=True, write_only=True)
    file = MyCustomBase64FileField(required=False)

    class Meta:
        model = Message
        fields = (
            'id', 'chat', 'sender', 'receiver', 'text', 'pub_date', 'file'
        )

    def create(self, validated_data):
        validated_data.pop('receiver', None)
        return super().create(validated_data)
