from rest_framework import serializers

from api.serializers.order_serializers import OrderWriteSerializer
from api.serializers.user_serializers import UserProfileSerializer
from job.models import FavoriteOrder


class FavoriteOrderSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    order = OrderWriteSerializer()

    class Meta:
        model = FavoriteOrder
        fields = '__all__'
