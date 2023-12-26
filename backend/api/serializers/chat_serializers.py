from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from api.serializers.user_serializers import UserChatAndMessageSerializer
from job.models import Chat


class ChatReadSerializer(serializers.ModelSerializer):
    """Сериализатор для метода get для чатов."""

    initiator = UserChatAndMessageSerializer(read_only=True)
    receiver = UserChatAndMessageSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ('id', 'initiator', 'receiver', 'last_message')

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-pub_date').first()
        if last_message:
            return (f'{last_message.text[:settings.MESSAGE_STR]}')
        else:
            return ''


class ChatCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания чата."""

    class Meta:
        model = Chat
        fields = ('receiver',)

    def validate(self, data):
        initiator = self.context.get('request').user
        receiver = data.get('receiver')
        if initiator == receiver:
            raise ValidationError('Нельзя создавать чат с самим собой.')
        if Chat.objects.filter(
            initiator=initiator,
            receiver=receiver
        ).exists():
            raise ValidationError(
                detail='Чат уже существует.'
            )
        if Chat.objects.filter(
            initiator=receiver,
            receiver=initiator
        ).exists():
            raise ValidationError(
                detail='Чат уже существует.'
            )
        data['initiator'] = initiator
        return data

    def to_representation(self, instance):
        serializer = ChatReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data
