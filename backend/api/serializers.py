from typing import Dict

from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from job.models import Chat, Message
from users.models import Subscription, User


class UserProfileSerializer(UserSerializer):
    """
    Сериализатор профиля пользователя.

    Атрибуты:
        is_subscribed (SerializerMethodField): поле, указывающее,
        подписан ли текущий пользователь на автора.

    Методы:
        get_is_subscribed(obj: User) -> bool: возвращает True,
        если текущий пользователь подписан на автора, иначе False.

    """

    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj: User) -> bool:
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.subscriber.filter(author=obj).exists()


class UserProfileCreateSerializer(UserCreateSerializer):
    """
    Сериализатор для создания пользователя.

    """

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class SubscriptionSerializer(UserProfileSerializer):
    """
    Сериализатор для подписки на автора.

    Атрибуты:
        email: адрес электронной почты пользователя.
        username: имя пользователя.
        first_name: имя пользователя.
        last_name: фамилия пользователя.
        is_subscribed: подписка.

    Методы:
        validate: метод для валидации данных при создании подписки.

    """

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
        read_only_fields = ('email', 'username')

    def validate(self, data: Dict) -> Dict:
        author = self.instance
        user = self.context.get('request').user
        subscription_exists = Subscription.objects.filter(
            author=author, user=user
        ).exists()

        if subscription_exists:
            raise serializers.ValidationError(
                {'subscription': ['Подписка уже есть']}
            )
        if user == author:
            raise serializers.ValidationError(
                {'subscription': ['Нельзя подписаться на себя']}
            )
        return data


class ChatReadSerializer(serializers.ModelSerializer):
    """Сериализатор для метода get для чатов."""

    initiator = UserProfileSerializer(read_only=True)
    receiver = UserProfileSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = ('id', 'initiator', 'receiver')


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
            raise serializers.ValidationError(
                detail='Чат уже существует.'
            )
        if Chat.objects.filter(
            initiator=receiver,
            receiver=initiator
        ).exists():
            raise serializers.ValidationError(
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


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор сообщения."""

    sender = UserProfileSerializer(read_only=True)
    chat = ChatReadSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'chat', 'sender', 'text', 'pub_date')
