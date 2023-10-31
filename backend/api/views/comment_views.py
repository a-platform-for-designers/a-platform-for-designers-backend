from api.serializers.comment_serializers import CommentSerializer
from job.models import Comment


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post')
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
