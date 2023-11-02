from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import PrimaryKeyRelatedField

from api.serializers.instrument_serializers import InstrumentSerializer
from api.serializers.skill_serializers import SkillSerializer
from job.models import Instrument, Resume, Skill


class ResumeReadSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    instruments = InstrumentSerializer(many=True)

    class Meta:
        model = Resume
        fields = ('id', 'instruments', 'skills', 'about')


class ResumeWriteSerializer(serializers.ModelSerializer):
    skills = PrimaryKeyRelatedField(queryset=Skill.objects.all(), many= True)
    instruments = PrimaryKeyRelatedField(queryset=Instrument.objects.all(), many=True)

    class Meta:
        model = Resume
        fields = ('id', 'instruments', 'skills', 'about', 'status')

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
