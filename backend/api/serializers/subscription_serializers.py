from typing import Dict

from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.validators import UniqueTogetherValidator

from .specialization_serializers import SpecializationSerializer
from .user_serializers import UserProfileSerializer
from users.models import Subscription


User = get_user_model()


class SubscriptionSerializer(UserProfileSerializer):
    """
    Сериализатор для подписки на автора. Расширяет UserProfileSerializer,
    добавляя возможность управления подписками пользователей.

    Атрибуты:
        email (str): Адрес электронной почты пользователя.
        username (str): Имя пользователя.
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        is_subscribed (bool): Статус подписки на автора.
        photo (str): Ссылка на фото пользователя.
        specialization (str): Специализация пользователя.

    Методы:
        validate (Dict): Валидирует данные, проверяя наличие
        уже существующей подписки и возможность подписаться на себя.

    Примечание:
        Использует модель User для определения полей сериализатора.
    """
    specialization = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'first_name',
                  'last_name', 'is_subscribed',
                  'photo', 'specialization')
        read_only_fields = ('email',)

    def get_specialization(self, obj):

        if hasattr(obj, 'profiledesigner'):

            profile_designer = obj.profiledesigner
            serializer = SpecializationSerializer(
                profile_designer.specialization, many=True
                )
            return serializer.data
        return None

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
    """
    Сериализатор для создания подписки на автора.
    Позволяет создавать новую подписку, проверяя уникальность
    сочетания пользователя и автора.

    Методы:
        validate (Dict): Проверяет, не пытается ли пользователь
        подписаться на себя и уникальность подписки.

    Примечание:
        Использует модель Subscription для определения полей
        и валидаторов сериализатора.

    """
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
