from rest_framework import viewsets, response
from rest_framework.decorators import action

from api.serializers.caseimage_serializers import CaseImageSerializer
from job.models import CaseImage


class CaseImageViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch']
    queryset = CaseImage.objects.all()
    serializer_class = CaseImageSerializer

    # @action(detail=True, methods=['get'])
    # def portfolio(self, request, pk=None):
    #     cover = CaseImage.objects.get(pk=pk)
    #     # Далее вы можете что-то сделать с cover
    #     # Например, сериализовать его и вернуть в ответе
    #     serializer = self.get_serializer(cover)
    #     return response.Response(serializer.data)
