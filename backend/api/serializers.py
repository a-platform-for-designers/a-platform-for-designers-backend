from typing import Dict

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from job.models import CaseImage, Comment, FavoriteOrder, Sphere, Case, Favorite, Instrument, Skill
from users.models import Subscription

User = get_user_model()


MIN_AMOUNT = 1
MAX_AMOUNT = 1000


class InstrumentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Instrument."""
    class Meta:
        model = Instrument
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Skill."""
    class Meta:
        model = Skill
        fields = '__all__'


class CaseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Case."""
    instrument = InstrumentSerializer(many=True)
    skill = SkillSerializer(many=True)
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited')

    class Meta:
        model = Case
        fields = [
            'id',
            'skills',
            'author',
            'title',
            'sphere',
            'instruments',
            'working_term',
            'description',
            'is_favorited',
        ]

    def get_is_favorited(self, obj):
        """проверка на добавление проекта в избранное"""
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            case=obj, user=request.user).exists()


class CaseShortSerializer(serializers.ModelSerializer):
    """"Сериализатор для добавления в избранное"""

    class Meta:
        model = Case
        fields = (
            'id',
            'title',
            'image',
            'working_term',
        )


class CaseCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    working_term = serializers.IntegerField(
        min_value=MIN_AMOUNT,
        max_value=MAX_AMOUNT
    )
    instrument = serializers.PrimaryKeyRelatedField(
        queryset=Instrument.objects.all(), many=True)
    skill = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True)

    class Meta:
        model = Case
        fields = ('instrument',
                  'skill',
                  'image',
                  'title',
                  'description',
                  'working_term',
                  )

    def create(self, validated_data):
        instrument = validated_data.pop('instrument')
        instance = super().create(validated_data)
        self.update_instrument(instance, instrument)
        return instance

    def update(self, instance, validated_data):
        instrument = validated_data.pop('instrument')
        instance = super().update(instance, validated_data)
        self.update_ingredients(instance, instrument)
        return instance

    def to_representation(self, instance):
        return CaseSerializer(instance).data


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


# заглушка
class CaseSerializer():
    pass

# заглушка
class OrderSerializer():
    pass


class CaseImageSerializer(serializers.ModelSerializer):
    case = CaseSerializer()
    is_avatar = SerializerMethodField(read_only=True)
    picture = Base64ImageField()

    class Meta:
        model = CaseImage
        fields = '__all__'


class CaseImageShortSerializer(serializers.ModelSerializer):
    picture = Base64ImageField()

    class Meta:
        model = CaseImage
        fields = ('picture', )


class CommentSerializer(serializers.ModelSerializer):
    case = CaseSerializer()
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class FavoriteOrderSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    order = OrderSerializer()

    class Meta:
        model = FavoriteOrder


class SphereSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sphere
        fields = '__all__'