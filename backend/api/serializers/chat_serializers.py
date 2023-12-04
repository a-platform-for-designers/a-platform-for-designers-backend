from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from api.serializers.message_serializers import MessageSerializer
from api.serializers.user_serializers import UserProfileSerializer
from job.models import Chat


class ChatReadSerializer(serializers.ModelSerializer):
    """Сериализатор для метода get для чатов."""

    initiator = UserProfileSerializer(read_only=True)
    receiver = UserProfileSerializer(read_only=True)
    # last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ('id', 'initiator', 'receiver')

    # def get_last_message(self, instance):
    #     message = instance.message_set.first()
    #     return MessageSerializer(instance=message)


class ChatCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания чата."""

    initiator = UserProfileSerializer()
    receiver = UserProfileSerializer()
    # message_set = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ['initiator', 'receiver']

    # class Meta:
    #     model = Chat
    #     fields = ('receiver',)

    # def validate(self, data):
    #     initiator = self.context.get('request').user
    #     receiver = data.get('receiver')
    #     if initiator == receiver:
    #         raise ValidationError('Нельзя создавать чат с самим собой.')
    #     if Chat.objects.filter(
    #         initiator=initiator,
    #         receiver=receiver
    #     ).exists():
    #         raise ValidationError(
    #             detail='Чат уже существует.'
    #         )
    #     if Chat.objects.filter(
    #         initiator=receiver,
    #         receiver=initiator
    #     ).exists():
    #         raise ValidationError(
    #             detail='Чат уже существует.'
    #         )
    #     data['initiator'] = initiator
    #     return data

    # def to_representation(self, instance):
    #     serializer = ChatReadSerializer(
    #         instance,
    #         context={'request': self.context.get('request')}
    #     )
    #     return serializer.data
