from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.db import transaction

from api.serializers.instrument_serializers import InstrumentSerializer
from api.serializers.skill_serializers import SkillSerializer
from job.models import Case, FavoriteCase, Instrument, Skill, CaseImage
from api.serializers.user_serializers import UserSerializer


MIN_AMOUNT = 1
MAX_AMOUNT = 1000


class CaseImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = CaseImage
        fields = ('image', )


class CaseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Case."""
    instruments = InstrumentSerializer(many=True)
    skills = SkillSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    images = CaseImageSerializer(many=True)

    class Meta:
        model = Case
        fields = [
            'id',
            'skills',
            'author',
            'title',
            'sphere',
            'instruments',
            'working_term',
            'description',
            'is_favorited',
            'images'
        ]

    def get_is_favorited(self, obj):
        """проверка на добавление проекта в избранное."""
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return FavoriteCase.objects.filter(
            case=obj, user=request.user).exists()


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
    author = UserSerializer(read_only=True)
    # avatar = Base64ImageField()
    images = CaseImageSerializer(many=True)
    # uploaded_images = serializers.ListField(
    #     child=serializers.ImageField(allow_empty_file=False, use_url=False),
    #     write_only=True
    # )

    class Meta:
        model = Case
        fields = ('sphere',
                  'instruments',
                  'skills',
                  'title',
                  'description',
                  'working_term',
                  'images',
                  'author',
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
        # instruments = validated_data.pop('instruments')
        images = validated_data.pop('images')
        instruments = validated_data.pop('instruments')
        skills = validated_data.pop('skills')
        author = self.context['request'].user
        case = Case.objects.create(**validated_data)
        case.instruments.set(instruments)
        # print('AAA', author)
        # print(validated_data)
        # print(images)
        # for image in uploaded_images:
        #     CaseImage.objects.create(case=case, image=image)


        self.add_images(case=case, images=images)

        return case

class CaseShowPortfolioSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaseImage
        fileds = '__all__'
