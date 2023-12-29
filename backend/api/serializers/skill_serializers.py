from rest_framework import serializers

from job.models import Skill


class SkillSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Skill.

    """
    class Meta:
        model = Skill
        fields = '__all__'
