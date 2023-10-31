from rest_framework.validators import UniqueTogetherValidator

from job.models import Like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Like.objects.all(),
                fields=['liker', 'author'],
                message='Лайк уже поставлен'
            )
        ]
