from api.serializers.case_serializers import CaseSerializer
from api.serializers.user_serializers import UserProfileSerializer

from job.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    case = CaseSerializer()
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
