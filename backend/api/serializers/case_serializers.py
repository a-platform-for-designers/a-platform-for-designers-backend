from rest_framework.fields import SerializerMethodField
from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from api.serializers.instrument_serializers import InstrumentSerializer
from api.serializers.skill_serializers import SkillSerializer
from job.models import Instrument, Skill
from job.models import Case, FavoriteCase, Instrument, Skill, CaseImage


MIN_AMOUNT = 1
MAX_AMOUNT = 1000


class InstrumentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Instrument."""
    class Meta:
        model = Instrument
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Skill."""
    class Meta:
        model = Skill
        fields = '__all__'


class CaseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Case."""
    instruments = InstrumentSerializer(many=True, required=False)
    skills = SkillSerializer(many=True, required=False)
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited')

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
            # 'id',
            'instruments',
            'skills',
            # 'image',
            'title',
            'description',
            'working_term',
        )


class CaseCreateSerializer(serializers.ModelSerializer):

    image = Base64ImageField(required=False)
    working_term = serializers.IntegerField(
        min_value=MIN_AMOUNT,
        max_value=MAX_AMOUNT
    )
    instruments = serializers.PrimaryKeyRelatedField(
        queryset=Instrument.objects.all(), many=True, required=False)
    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True, required=False)

    class Meta:
        model = Case
        fields = ('id',
                  'skills',
                  'author',
                  'title',
                  'sphere',
                  'instruments',
                  'working_term',
                  'description',
                  'image',
                  )


class CaseShowPortfolioSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaseImage
        fileds = '__all__'
