from job.models import Language, Like, Order, Resume, Specialization
from djoser.serializers import UserSerializer

from typing import Dict
from django.contrib.auth import get_user_model
from djoser.serializers import (
    UserCreateSerializer, UserSerializer, ValidationError
)
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator

from rest_framework import serializers
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


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'


class ResumeReadSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    instruments = InstrumentSerializer(many=True)

    class Meta:
        model = Resume
        fields = ('description', 'instruments', 'skills')


class ResumeWriteSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    instruments = InstrumentSerializer(many=True)

    class Meta:
        model = Resume
        fields = '__all__'

    def validate_skills(self, value):
        if not value:
            raise ValidationError('Укажите хотя бы один навык')
        if len(set(value)) != len(value):
            raise ValidationError('Навыки не должны повторяться')
        return value

    def validate_instruments(self, value):
        if not value:
            raise ValidationError('Укажите хотя бы один инструмент')
        if len(set(value)) != len(value):
            raise ValidationError('Ингредиенты не должны повторяться')
        return value


class OrderSerializer(serializers.ModelSerializer):
    specialization = SpecializationSerializer()
    sphere = SphereSerializer()
    skills = SkillSerializer(many=True)
    instruments = InstrumentSerializer(many=True)
    is_favorited_order = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = '__all__'
    
    def validate_skills(self, value):
        if not value:
            raise ValidationError('Укажите хотя бы один навык')
        if len(set(value)) != len(value):
            raise ValidationError('Навыки не должны повторяться')
        return value

    def validate_instruments(self, value):
        if not value:
            raise ValidationError('Укажите хотя бы один инструмент')
        if len(set(value)) != len(value):
            raise ValidationError('Ингредиенты не должны повторяться')
        return value
    
    def validate_sphere(self, value):
        if not value:
            raise ValidationError('Укажите сферу заказа')
    
    def validate_specialization(self, value):
        if not value:
            raise ValidationError('Укажите спемиализацию заказа')
    
    def get_is_favorited_order(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return FavoriteOrder.objects.filter(
            viewer=request.user, order=obj
        ).exists()


class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Like.objects.all(),
                fields=['liker', 'author'],
                message='Лайк уже поставлен'
            )
        ]