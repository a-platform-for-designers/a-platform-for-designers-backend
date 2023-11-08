from rest_framework import serializers

from api.serializers.chat_serializers import ChatReadSerializer
from api.serializers.user_serializers import UserShortSerializer

from job.models import Message


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор сообщения."""

    sender = UserShortSerializer(read_only=True)
    chat = ChatReadSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'chat', 'sender', 'text', 'pub_date')
