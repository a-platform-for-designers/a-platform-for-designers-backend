from rest_framework import serializers
# from rest_framework.fields import SerializerMethodField
# from rest_framework.exceptions import ValidationError
# from rest_framework.serializers import PrimaryKeyRelatedField

from api.serializers.instrument_serializers import InstrumentSerializer
from api.serializers.skill_serializers import SkillSerializer
from job.models import Mentoring
from users.models import User


class MentoringReadSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, source='user.profiledesigner.skills')
    instruments = InstrumentSerializer(
        many=True,
        source='user.profiledesigner.instruments'
    )

    class Meta:
        model = Mentoring
        fields = (
            'id',
            'instruments',
            'skills',
            'experience',
            'expertise',
            'price',
            'agreement_free'
        )


class MentoringWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mentoring
        fields = ('id', 'experience', 'expertise', 'price', 'agreement_free')

    def validate(self, data):
        if data.get('price') and data.get('agreement_free'):
            raise serializers.ValidationError(
                "Какое то из полей price/agreement_free должно быть пустым"
            )
        if not data.get('price') and not data.get('agreement_free'):
            raise serializers.ValidationError(
                "Какое то из полей price/agreement_free должно быть заполнено"
            )
        return data

    def create(self, validated_data):
        user = self.context.get('request').user
        try:
            mentoring = user.mentoring
            if validated_data.get('price') and mentoring.agreement_free:
                mentoring.agreement_free = None
            if validated_data.get('agreement_free') and mentoring.price:
                mentoring.price = None
            for attr, value in validated_data.items():
                setattr(mentoring, attr, value)
            mentoring.save()
            return mentoring
        except Mentoring.DoesNotExist:
            return super().create(validated_data)


class MentorSerializer(serializers.ModelSerializer):
    mentoring = MentoringReadSerializer()
    country = serializers.CharField(source='profiledesigner.country')

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'photo',
            'country',
            'mentoring'
        )
