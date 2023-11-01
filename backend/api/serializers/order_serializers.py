from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from api.serializers.instrument_serializers import InstrumentSerializer
from api.serializers.skill_serializers import SkillSerializer
from api.serializers.specialization_serializers import SpecializationSerializer
from api.serializers.sphere_serializers import SphereSerializer
from job.models import FavoriteOrder, Order


class OrderSerializer(serializers.ModelSerializer):
    specialization = SpecializationSerializer()
    sphere = SphereSerializer()
    skills = SkillSerializer(many=True)
    instruments = InstrumentSerializer(many=True)
    is_favorited_order = SerializerMethodField()

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
