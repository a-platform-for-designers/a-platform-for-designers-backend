from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from typing import Dict
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.serializers.user_serializers import UserProfileSerializer

from job.models import Case, Favorite, Instrument, Skill, Chat, Message

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
