from api.serializers.language_serializers import LanguageSerializer
from job.models import Language


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer