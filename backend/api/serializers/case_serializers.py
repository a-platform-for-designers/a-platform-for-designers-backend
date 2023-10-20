from rest_framework import serializers
from job.models import Case, Instrument, Skill


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

    class Meta:
        model = Case
        fields = [
            'id',
            'skills',
            'title',
            'sphere',
            'instruments',
            'working_term'
        ]