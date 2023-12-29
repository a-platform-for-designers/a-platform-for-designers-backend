from rest_framework import serializers

from job.models import Specialization


class SpecializationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для специализаций дизайнера.

    """
    class Meta:
        model = Specialization
        fields = '__all__'
