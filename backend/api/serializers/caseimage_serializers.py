from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from job.models import CaseImage


class CaseImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = CaseImage
        fields = ('id', 'image', )
