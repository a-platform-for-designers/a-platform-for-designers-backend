from rest_framework import serializers

from api.serializers.chat_serializers import ChatReadSerializer
from api.serializers.user_serializers import UserChatAndMessageSerializer

from job.models import Message


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор сообщения."""

    sender = UserChatAndMessageSerializer(read_only=True)
    chat = ChatReadSerializer(read_only=True)
    receiver = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = Message
        fields = ('id', 'chat', 'sender', 'receiver', 'text', 'pub_date')

    def create(self, validated_data):
        validated_data.pop('receiver', None)
        return super().create(validated_data)
