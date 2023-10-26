from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from drf_extra_fields.fields import Base64ImageField
from job.models import CaseImage, Comment, FavoriteOrder, Sphere
from api.serializers.user_serializers import UserProfileSerializer

# заглушка
class CaseSerializer():
    pass

# заглушка
class OrderSerializer():
    pass


class CaseImageSerializer(serializers.ModelSerializer):
    case = CaseSerializer()
    is_avatar = SerializerMethodField(read_only=True)
    picture = Base64ImageField()

    class Meta:
        model = CaseImage
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    case = CaseSerializer()
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class FavoriteOrderSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    order = OrderSerializer()

    class Meta:
        model = FavoriteOrder


class SphereSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sphere
        fields = '__all__'
