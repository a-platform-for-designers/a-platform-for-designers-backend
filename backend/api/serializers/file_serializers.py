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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        file_url = representation['file']
        file_name = file_url.split('/')[-1]  # получаем имя файла из полного пути
        representation['file'] = f'/media/messages/{file_name}' # заменяем полный путь на нужный формат
        return representation
