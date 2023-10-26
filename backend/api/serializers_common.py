from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from drf_extra_fields.fields import Base64ImageField
from job.models import CaseImage

# заглушка
class CaseSerializer():
    pass

class CaseImageSerializer(serializers.ModelSerializer):
    case = CaseSerializer()
    is_avatar = SerializerMethodField(read_only=True)
    picture = Base64ImageField()

    class Meta:
        model = CaseImage
        fields = '__all__'