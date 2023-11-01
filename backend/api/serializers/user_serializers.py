from django.contrib.auth import get_user_model

from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from drf_extra_fields.fields import Base64ImageField

from users.models import ProfileCustomer, ProfileDesigner


User = get_user_model()


class ProfileCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileCustomer
        fields = ('id', 'user', 'post')


class ProfileDesignerSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ['id']
        model = ProfileDesigner
        fields = (
            'id',
            'user',
            'education',
            'country',
            'specialization',
            'hobby',
            'language'
        )


class UserProfileSerializer(UserSerializer):
    """
    Сериализатор профиля пользователя.

    Атрибуты:
        is_subscribed (SerializerMethodField): поле, указывающее,
        подписан ли текущий пользователь на автора.

    Методы:
        get_is_subscribed(obj: User) -> bool: возвращает True,
        если текущий пользователь подписан на автора, иначе False.
    Внимание! Код картинки для регистрации пользователя через json:
    iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVQI12P4//8/AAX+Av7czFnnAAAAAElFTkSuQmCC

    """
    profilecustomer = ProfileCustomerSerializer(read_only=True)
    profiledesigner = ProfileDesignerSerializer(read_only=True)
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        ordering = ['id']
        model = User
        fields = (
            'email',
            'id',
            'first_name',
            'last_name',
            'is_subscribed',
            'photo',
            'description',
            'is_customer',
            'profilecustomer',
            'profiledesigner'
        )

    def get_is_subscribed(self, obj: User) -> bool:
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.subscriber.filter(author=obj).exists()


class UserProfileCreateSerializer(UserCreateSerializer):
    """
    Сериализатор для создания пользователя.

    """
    photo = Base64ImageField()

    class Meta:
        ordering = ['id']
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'photo',
            'description',
            'is_customer'
        )
        required_fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'is_customer'
        )

    def __init__(self, *args, **kwargs):
        super(UserProfileCreateSerializer, self).__init__(*args, **kwargs)
        for field in self.Meta.required_fields:
            self.fields[field].required = True
