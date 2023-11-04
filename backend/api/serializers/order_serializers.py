from djoser.serializers import UserSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import PrimaryKeyRelatedField

from api.serializers.instrument_serializers import InstrumentSerializer
from api.serializers.skill_serializers import SkillSerializer
from api.serializers.specialization_serializers import SpecializationSerializer
from api.serializers.sphere_serializers import SphereSerializer
from job.models import (
    FavoriteOrder, Instrument, Order, Skill, Specialization, Sphere
)


class OrderReadSerializer(ModelSerializer):
    specialization = SpecializationSerializer()
    customer = UserSerializer()
    sphere = SphereSerializer()
    skills = SkillSerializer(many=True)
    instruments = InstrumentSerializer(many=True)
    is_favorited_order = SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'customer',
            'title',
            'specialization',
            'price_min',
            'price_max',
            'currency',
            'sphere',
            'skills',
            'instruments',
            'description',
            'is_favorited_order'
        )

    def get_is_favorited_order(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return FavoriteOrder.objects.filter(
            user=request.user, order=obj
        ).exists()


class OrderWriteSerializer(ModelSerializer):
    specialization = PrimaryKeyRelatedField(
        queryset=Specialization.objects.all()
    )
    sphere = PrimaryKeyRelatedField(queryset=Sphere.objects.all())
    skills = PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)
    instruments = PrimaryKeyRelatedField(
        queryset=Instrument.objects.all(),
        many=True
    )

    class Meta:
        model = Order
        fields = (
            'id',
            'title',
            'specialization',
            'price_min',
            'price_max',
            'currency',
            'sphere',
            'skills',
            'instruments',
            'description',
        )

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
            raise ValidationError('Инструменты не должны повторяться')
        return value
