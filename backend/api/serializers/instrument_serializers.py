from rest_framework import serializers

from job.models import Instrument


class InstrumentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Instrument.

    """
    class Meta:
        model = Instrument
        fields = '__all__'
