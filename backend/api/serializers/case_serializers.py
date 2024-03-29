from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.db import transaction

from api.serializers.instrument_serializers import InstrumentSerializer
from api.serializers.sphere_serializers import SphereSerializer
from api.serializers.specialization_serializers import SpecializationSerializer
from api.serializers.caseimage_serializers import CaseImageSerializer
from job.models import Case, FavoriteCase, CaseImage
from api.serializers.user_serializers import AuthorSerializer


class CaseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Case."""
    author = AuthorSerializer()
    instruments = InstrumentSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    specialization = SpecializationSerializer()
    # is_like = serializers.SerializerMethodField()
    images = CaseImageSerializer(many=True)
    avatar = Base64ImageField()
    sphere = SphereSerializer()

    class Meta:
        model = Case
        fields = [
            'id',
            'author',
            'title',
            'instruments',
            'sphere',
            'avatar',
            'images',
            'working_term',
            'description',
            'is_favorited',
            'specialization'
            # 'is_like'
        ]

    def get_is_favorited(self, obj) -> bool:
        """проверка на добавление проекта в избранное."""
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return FavoriteCase.objects.filter(
            case=obj, user=request.user).exists()

    # def get_is_like(self, obj) -> bool:
    #     """проверка на добавление проекта в лайки."""
    #     request = self.context.get('request')
    #     if request.user.is_anonymous:
    #         return False
    #     return Like.objects.filter(
    #         author=obj.author).exists()


class CaseShortSerializer(serializers.ModelSerializer):
    """"Сериализатор для добавления в избранное"""

    class Meta:
        model = Case
        fields = (
            'instruments',
            'skills',
            'title',
            'description',
            'working_term',
        )


class CaseCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    avatar = Base64ImageField()
    author = AuthorSerializer(read_only=True)
    images = CaseImageSerializer(many=True)

    class Meta:
        model = Case
        fields = (
            'id',
            'author',
            'title',
            'specialization',
            'instruments',
            'sphere',
            'avatar',
            'images',
            'working_term',
            'description',
        )

    @staticmethod
    def add_images(case, images):
        CaseImage.objects.bulk_create(
            [
                CaseImage(
                    image=image['image'],
                    case=case,
                ) for image in images
            ]
        )

    @transaction.atomic
    def create(self, validated_data):
        instruments = validated_data.pop('instruments', [])
        if len(instruments) > 5:
            raise serializers.ValidationError("Количество инструментов не "
                                              "должно превышать 5.")

        images = validated_data.pop('images')
        case = Case.objects.create(**validated_data)
        case.instruments.set(instruments)
        self.add_images(case=case, images=images)
        return case

    def update(self, instance, validated_data):
        instruments_data = validated_data.pop('instruments', [])
        images_data = validated_data.pop('images', [])

        instance = super().update(instance, validated_data)

        instance.instruments.clear()
        instance.instruments.add(*instruments_data)

        CaseImage.objects.filter(case=instance).delete()
        self.add_images(instance, images_data)

        return instance


class CaseFavoriteShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Case
        fields = ('id', 'title', 'avatar')
