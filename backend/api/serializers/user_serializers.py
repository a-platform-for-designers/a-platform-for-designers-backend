from django.contrib.auth import get_user_model

from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import PrimaryKeyRelatedField
from drf_extra_fields.fields import Base64ImageField

from api.serializers.instrument_serializers import InstrumentSerializer
from api.serializers.skill_serializers import SkillSerializer
from api.serializers.language_serializers import LanguageSerializer
from api.serializers.resume_serializers import ResumeReadSerializer
from api.serializers.specialization_serializers import SpecializationSerializer
from users.models import ProfileCustomer, ProfileDesigner
from job.models import Case, Specialization, Language, Instrument, Skill


User = get_user_model()


def check_photo(validated_data, user):
    if 'photo' in validated_data:
        photo = validated_data.pop('photo')
        user.photo = photo
        user.save()


class TokenResponseSerializer(serializers.Serializer):
    auth_token = serializers.CharField()


class ProfileCustomerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    photo = Base64ImageField(required=False)
    country = serializers.CharField()
    about = serializers.CharField()

    class Meta:
        model = ProfileCustomer
        fields = ('id', 'post', 'photo', 'country', 'about')

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("Нужны хоть какие-то данные!")
        return data

    def create(self, validated_data):
        user = self.context.get('request').user

        check_photo(validated_data, user)

        try:
            profilecustomer = user.profilecustomer
            for attr, value in validated_data.items():
                setattr(profilecustomer, attr, value)
            profilecustomer.save()
            return profilecustomer
        except ProfileCustomer.DoesNotExist:
            return super().create(validated_data)


class ProfileDesignerSerializer(serializers.ModelSerializer):
    specialization = SpecializationSerializer(many=True)
    language = LanguageSerializer(many=True)
    instruments = InstrumentSerializer(many=True)
    skills = SkillSerializer(many=True)

    class Meta:
        model = ProfileDesigner
        fields = (
            'id',
            'education',
            'country',
            'work_status',
            'specialization',
            'language',
            'instruments',
            'skills',
            'about',
        )


class ProfileDesignerCreateSerializer(serializers.ModelSerializer):
    specialization = PrimaryKeyRelatedField(
        queryset=Specialization.objects.all(),
        many=True,
        required=False,
    )
    language = PrimaryKeyRelatedField(
        queryset=Language.objects.all(),
        many=True,
        required=False,
    )
    instruments = PrimaryKeyRelatedField(
        queryset=Instrument.objects.all(),
        many=True,
        required=False,
    )
    skills = PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        required=False,
    )
    photo = Base64ImageField(required=False)

    class Meta:
        model = ProfileDesigner
        fields = (
            'id',
            'education',
            'country',
            'work_status',
            'specialization',
            'language',
            'instruments',
            'skills',
            'about',
            'photo',
        )

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("Нужны хоть какие-то данные!")
        return data

    def create(self, validated_data):
        user = self.context.get('request').user

        check_photo(validated_data, user)

        try:
            profiledesigner = user.profiledesigner
            language = validated_data.pop('language', [])
            specialization = validated_data.pop('specialization', [])
            instruments = validated_data.pop('instruments', [])
            skills = validated_data.pop('skills', [])

            for attr, value in validated_data.items():
                setattr(profiledesigner, attr, value)

            if language:
                profiledesigner.language.set(language)
            if specialization:
                profiledesigner.specialization.set(specialization)
            if instruments:
                profiledesigner.instruments.set(instruments)
            if skills:
                profiledesigner.skills.set(skills)

            profiledesigner.save()
            return profiledesigner

        except ProfileDesigner.DoesNotExist:
            return super().create(validated_data)


class PortfolioSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = Case
        fields = (
            'id',
            'avatar',
        )


class UserProfileSerializer(UserSerializer):

    profilecustomer = ProfileCustomerSerializer(read_only=True)
    profiledesigner = ProfileDesignerSerializer(read_only=True)
    is_subscribed = SerializerMethodField(read_only=True)
    date_joined = serializers.SerializerMethodField()
    portfolio = serializers.SerializerMethodField()

    class Meta:
        ordering = ['id']
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'is_subscribed',
            'photo',
            'date_joined',
            'is_customer',
            'profilecustomer',
            'profiledesigner',
            'portfolio'
        )

    def get_date_joined(self, obj):
        return f'Published {obj.date_joined.strftime("%d %B %Y")}'

    def get_is_subscribed(self, obj: User) -> bool:
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.subscriber.filter(author=obj).exists()

    def get_portfolio(self, obj):
        cases = Case.objects.filter(author=obj)
        return PortfolioSerializer(cases, many=True).data

    # def get_profilecustomer(self, obj):
    #     obj=ProfileCustomer.objects.filter(user=obj)
    #     if obj.exists():
    #         return ProfileCustomerSerializer(obj).data
    #     else:
    #         return {'id':0, 'post': ''}

    # def get_profiledesigner(self, obj):
    #     obj=ProfileDesigner.objects.filter(user=obj)
    #     if obj.exists():
    #         return ProfileDesignerSerializer(obj).data
    #     else:
    #         return {
    #                 'id':0, 'education': '',
    #                 'country': '',
    #                 'specialization': 0,
    #                 'hobby': '',
    #                 'language':[]
    #          }

    # def get_resume(self, obj):
    #     if obj.resume:
    #         return ResumeReadSerializer(obj.resume).data
    #     else:
    #         return {'id': 0, 'skills':[], 'instruments': [], 'about':[]}


class UserProfileCreateSerializer(UserCreateSerializer):
    """
    Сериализатор для создания пользователя.

    """
    id = serializers.IntegerField(read_only=True)

    class Meta:
        ordering = ['id']
        model = User
        fields = (
            'id',
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


class AuthorSerializer(UserSerializer):
    """
    Сериализатор для отображения пользователя в кейсе

    """
    specialization = SpecializationSerializer(
        many=True,
        source='profiledesigner.specialization'
    )

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'photo',
            'specialization',
        )


class ApplicantSerializer(AuthorSerializer):
    """
    Сериализатор для отображения пользователя в откликах

    """
    country = serializers.CharField(
        source='profiledesigner.country'
    )

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'photo',
            'specialization',
            'country'
        )


class AuthorListSerializer(AuthorSerializer):
    """
    Сериализатор для отображения пользователя в списке юзеров
    """
    country = SerializerMethodField(read_only=True)
    work_status = SerializerMethodField(read_only=True)
    about = SerializerMethodField(read_only=True)
    last_cases = SerializerMethodField(read_only=True)

    class Meta:
        ordering = ['id']
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'photo',
            'specialization',
            'country',
            'work_status',
            'about',
            'last_cases',
        )

    def get_country(self, obj) -> str:
        try:
            profile = ProfileDesigner.objects.get(user=obj)
            return str(profile.country)
        except ProfileDesigner.DoesNotExist:
            return ''

    def get_work_status(self, obj) -> bool:
        try:
            return obj.profiledesigner.work_status
        except ProfileDesigner.DoesNotExist:
            return False

    def get_about(self, obj) -> str:
        try:
            return obj.profiledesigner.about
        except ProfileDesigner.DoesNotExist:
            return ''

    def get_last_cases(self, obj) -> dict:
        from api.serializers.case_serializers import CaseSerializer
        cases = Case.objects.filter(author=obj)[:2]
        return CaseSerializer(
            cases,
            context={'request': self.context['request']},
            many=True
        ).data


class UserChatAndMessageSerializer(UserSerializer):
    """
    Сериализатор для отображения пользователя в чатах и сообщениях

    """
    class Meta:
        ordering = ['id']
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'photo',
        )


class CustomerSerializer(UserSerializer):
    """
    Сериализатор для отображения пользователя в откликах

    """
    post = serializers.CharField(source='profilecustomer.post')

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'photo',
            'post'
        )
