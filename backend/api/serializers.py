from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from typing import Dict
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.serializers.user_serializers import UserProfileSerializer

from job.models import Case, Favorite, Instrument, Skill, Chat, Message

from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from api.serializers.user_serializers import UserProfileSerializer
from job.models import (CaseImage, Comment, FavoriteOrder, Sphere, Case,
                        Favorite, Instrument, Skill, Language, Like,
                        Order, Resume, Specialization)


User = get_user_model()

MIN_AMOUNT = 1
MAX_AMOUNT = 1000

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'


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


class SphereSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sphere
        fields = '__all__'


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


class LikeSerializer(serializers.ModelSerializer):
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
