from djoser.serializers import UserSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_framework.fields import SerializerMethodField, IntegerField
from rest_framework.validators import UniqueTogetherValidator

from api.serializers.specialization_serializers import SpecializationSerializer
from api.serializers.sphere_serializers import SphereSerializer
from api.serializers.user_serializers import (
    ApplicantSerializer, CustomerSerializer
)
from job.models import (
    FavoriteOrder, Order, OrderResponse, Specialization, Sphere
)
from users.models import User


class OrderReadSerializer(ModelSerializer):
    specialization = SpecializationSerializer()
    customer = CustomerSerializer()
    sphere = SphereSerializer()
    is_responded_order = SerializerMethodField()
    is_favorited_order = SerializerMethodField()
    pub_date = SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'customer',
            'title',
            'specialization',
            'payment',
            'sphere',
            'description',
            'pub_date',
            'is_responded_order',
            'is_favorited_order',
            'is_published'
        )

    def get_pub_date(self, obj):
        return f'Published {obj.pub_date.strftime("%d %B %Y")}'

    def get_is_responded_order(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return OrderResponse.objects.filter(
            user=request.user, order=obj
        ).exists()

    def get_is_favorited_order(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return FavoriteOrder.objects.filter(
            user=request.user, order=obj
        ).exists()


class OrderAuthorReadSerializer(OrderReadSerializer):
    applicants = SerializerMethodField()
    customer = CustomerSerializer()

    class Meta:
        model = Order
        fields = (
            'id',
            'customer',
            'title',
            'specialization',
            'payment',
            'sphere',
            'description',
            'pub_date',
            'applicants',
        )

    def get_applicants(self, obj):
        responses = OrderResponse.objects.filter(order=obj).all()
        users = User.objects.filter(id__in=responses.values('user'))
        return ApplicantSerializer(
            users, many=True, context=self.context
        ).data


class OrderAuthorListReadSerializer(OrderReadSerializer):
    responses = SerializerMethodField()
    customer = CustomerSerializer()

    class Meta:
        model = Order
        fields = (
            'id',
            'customer',
            'title',
            'specialization',
            'payment',
            'sphere',
            'description',
            'pub_date',
            'responses',
        )

    def get_responses(self, obj):
        return OrderResponse.objects.filter(order=obj).count()


class OrderWriteSerializer(ModelSerializer):
    id = IntegerField(read_only=True)
    specialization = PrimaryKeyRelatedField(
        queryset=Specialization.objects.all()
    )
    customer = UserSerializer(read_only=True)
    sphere = PrimaryKeyRelatedField(queryset=Sphere.objects.all())

    class Meta:
        model = Order
        fields = (
            'id',
            'customer',
            'title',
            'specialization',
            'payment',
            'sphere',
            'description',
        )


class OrderResponseSerializer(ModelSerializer):
    class Meta:
        model = OrderResponse
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=OrderResponse.objects.all(),
                fields=['user', 'order'],
                message='Отклик уже сделан'
            )
        ]


class FavoriteOrderSerializer(ModelSerializer):
    class Meta:
        model = FavoriteOrder
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=FavoriteOrder.objects.all(),
                fields=['user', 'order'],
                message='Заказ уже добавлен в избранное'
            )
        ]
