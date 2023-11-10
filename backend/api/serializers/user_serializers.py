from django.contrib.auth import get_user_model

from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
# from rest_framework.fields import SerializerMethodField
from drf_extra_fields.fields import Base64ImageField

from api.serializers.resume_serializers import ResumeReadSerializer
from api.serializers.specialization_serializers import SpecializationSerializer
from users.models import ProfileCustomer, ProfileDesigner
from job.models import Specialization


User = get_user_model()


class TokenResponseSerializer(serializers.Serializer):
    auth_token = serializers.CharField()


class ProfileCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileCustomer
        fields = ('id', 'post')


class ProfileDesignerSerializer(serializers.ModelSerializer):
    specialization = SpecializationSerializer()

    class Meta:
        model = ProfileDesigner
        fields = (
            'id',
            'education',
            'country',
            'specialization',
            'hobby',
            'language'
        )

    def create(self, validated_data):
        specialization_data = validated_data.pop('specialization')
        specialization, created = Specialization.objects.get_or_create(
            **specialization_data
        )
        profile_designer = ProfileDesigner.objects.create(
            specialization=specialization,
            **validated_data
        )
        return profile_designer

    def update(self, instance, validated_data):
        specialization_data = validated_data.pop('specialization')
        specialization, created = Specialization.objects.get_or_create(
            **specialization_data
        )
        instance.specialization = specialization
        instance.education = validated_data.get(
            'education',
            instance.education
        )
        instance.country = validated_data.get('country', instance.country)
        instance.hobby = validated_data.get('hobby', instance.hobby)
        instance.language = validated_data.get('language', instance.language)
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    """
    Сериализатор профиля пользователя.

    """

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'photo',
            'is_customer',
            # 'specialization'
        )

    # def get_specialization(self, obj):
    #     if hasattr(obj, 'profiledesigner'):
    #         return obj.profiledesigner.specialization.name
    #     return None


class UserProfileSerializer(UserSerializer):
    """
    Сериализатор профиля пользователя.

    """

    profilecustomer = ProfileCustomerSerializer(read_only=True)
    profiledesigner = ProfileDesignerSerializer(read_only=True)
    # is_subscribed = SerializerMethodField(read_only=True)
    resume = ResumeReadSerializer(read_only=True)

    class Meta:
        ordering = ['id']
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'photo',
            'date_joined',
            'is_customer',
            # 'is_subscribed',
            'resume',
            'profiledesigner',
            'profilecustomer'
        )

    # def get_is_subscribed(self, obj: User) -> bool:
    #     user = self.context.get('request').user
    #     if user.is_anonymous:
    #         return False
    #     return user.subscriber.filter(author=obj).exists()


class UserProfileCreateSerializer(UserCreateSerializer):
    """
    Сериализатор для создания пользователя.

    """

    # photo = Base64ImageField()

    class Meta:
        ordering = ['id']
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
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


class UserProfileUpdateSerializer(serializers.ModelSerializer):

    photo = Base64ImageField()

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'photo'
        )
