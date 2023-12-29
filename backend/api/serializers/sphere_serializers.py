from rest_framework import serializers

from job.models import Sphere


class SphereSerializer(serializers.ModelSerializer):
    """
    Сериализатор для сфер деятельности дизайнера.

    """
    class Meta:
        model = Sphere
        fields = '__all__'
