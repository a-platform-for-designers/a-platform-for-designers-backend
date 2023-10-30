from job.models import Language, Like, Order, Resume, Specialization
from typing import Dict
from django.contrib.auth import get_user_model
from djoser.serializers import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers


User = get_user_model()


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