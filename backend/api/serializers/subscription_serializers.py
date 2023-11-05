from typing import Dict

from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.validators import UniqueTogetherValidator

from .user_serializers import UserProfileSerializer
from users.models import Subscription


User = get_user_model()


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
        fields = ('email', 'id', 'first_name',
                  'last_name', 'is_subscribed')
        read_only_fields = ('email',)

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


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['user', 'author'],
                message='Вы уже подписаны на этого пользователя!'
            )
        ]

    def validate(self, data):
        author = data.get('author')
        user = data.get('user')
        if user == author:
            raise serializers.ValidationError(
                detail='Вы не можете подписаться на самого себя!',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data
