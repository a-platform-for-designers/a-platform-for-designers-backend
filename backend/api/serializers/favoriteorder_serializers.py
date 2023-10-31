from api.serializers.order_serializers import OrderSerializer
from api.serializers.user_serializers import UserProfileSerializer
from job.models import FavoriteOrder


class FavoriteOrderSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    order = OrderSerializer()

    class Meta:
        model = FavoriteOrder
