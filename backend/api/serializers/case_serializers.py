from rest_framework import serializers

from api.serializers.instrument_serializers import InstrumentSerializer
from api.serializers.skill_serializers import SkillSerializer
from job.models import Case, FavoriteCase, Instrument, Skill, CaseImage


MIN_AMOUNT = 1
MAX_AMOUNT = 1000


class CaseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Case."""
    instruments = InstrumentSerializer(many=True)
    skills = SkillSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()

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
            'instruments',
            'skills',
            'title',
            'description',
            'working_term',
        )


class CaseCreateSerializer(serializers.ModelSerializer):
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
        fields = (
            'id',
            'skills',
            'title',
            'sphere',
            'instruments',
            'working_term',
            'description',
        )


class CaseShowPortfolioSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaseImage
        fileds = '__all__'