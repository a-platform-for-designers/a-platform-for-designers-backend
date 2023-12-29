from rest_framework import serializers

from api.serializers.user_serializers import UserChatAndMessageSerializer
from job.models import Chat, File


class FileSerializer(serializers.ModelSerializer):
    """
    Сериализатор файла.

    """
    sender = UserChatAndMessageSerializer(read_only=True)
    chat = serializers.PrimaryKeyRelatedField(
        queryset=Chat.objects.all(),
        required=True
    )
    file = serializers.FileField(required=True)

    class Meta:
        model = File
        fields = ('id', 'chat', 'sender', 'pub_date', 'file')
