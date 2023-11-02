from rest_framework.fields import SerializerMethodField
from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from api.serializers.instrument_serializers import InstrumentSerializer
from api.serializers.skill_serializers import SkillSerializer
from job.models import Instrument, Skill
from job.models import Case, Favorite, CaseImage


MIN_AMOUNT = 1
MAX_AMOUNT = 1000


class CaseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Case.

    """

    # instrument = InstrumentSerializer(many=True)
    # skill = SkillSerializer(many=True)
    # is_favorited = SerializerMethodField(
    #     method_name='get_is_favorited')

    class Meta:
        model = Case
        fields = [
            'id',
            # 'skill',
            'author',
            'title',
            'sphere',
            # 'instrument',
            'working_term',
            'description',
            # 'is_favorited',
        ]

    # def get_is_favorited(self, obj):
    #     """проверка на добавление проекта в избранное"""
    #     request = self.context.get('request')
    #     if request.user.is_anonymous:
    #         return False
    #     return Favorite.objects.filter(
    #         case=obj, user=request.user).exists()


class CaseShortSerializer(serializers.ModelSerializer):
    """"
    Сериализатор для добавления в избранное

    """

    class Meta:
        model = Case
        fields = (
            'id',
            'title',
            'image',
            'working_term',
        )


class CaseCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    working_term = serializers.IntegerField(
        min_value=MIN_AMOUNT,
        max_value=MAX_AMOUNT
    )
    instrument = serializers.PrimaryKeyRelatedField(
        queryset=Instrument.objects.all(), many=True)
    skill = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True)

    class Meta:
        model = Case
        fields = ('instrument',
                  'skill',
                  'image',
                  'title',
                  'description',
                  'working_term',
                  )

    def create(self, validated_data):
        instrument = validated_data.pop('instrument')
        instance = super().create(validated_data)
        self.update_instrument(instance, instrument)
        return instance

    def update(self, instance, validated_data):
        instrument = validated_data.pop('instrument')
        instance = super().update(instance, validated_data)
        self.update_ingredients(instance, instrument)
        return instance

    def to_representation(self, instance):
        return CaseSerializer(instance).data


class CaseShowPortfolioSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaseImage
        fileds = '__all__'
