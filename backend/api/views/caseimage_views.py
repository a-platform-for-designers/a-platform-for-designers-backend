from api.serializers.caseimage_serializers import CaseImageSerializer
from job.models import CaseImage


class CaseImageViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post')
    queryset = CaseImage.objects.all()
    serializer_class = CaseImageSerializer

    @action(detail=True,
            methods=['get', ])
    def portfolio(self, request, pk):        
        cover = CaseImage
