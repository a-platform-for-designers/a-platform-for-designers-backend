from drf_extra_fields.fields import Base64ImageField
from rest_framework.fields import SerializerMethodField

from api.serializers.case_serializers import CaseSerializer
from job.models import CaseImage


class CaseImageSerializer(serializers.ModelSerializer):
    case = CaseSerializer()
    is_avatar = SerializerMethodField(read_only=True)
    picture = Base64ImageField()

    class Meta:
        model = CaseImage
        fields = '__all__'


class CaseImageShortSerializer(serializers.ModelSerializer):
    picture = Base64ImageField()

    class Meta:
        model = CaseImage
        fields = ('picture', )
