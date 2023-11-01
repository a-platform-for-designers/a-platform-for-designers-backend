from rest_framework.permissions import AllowAny
from rest_framework import viewsets

from api.serializers.instrument_serializers import InstrumentSerializer
from job.models import Instrument


class InstrumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    pagination_class = None
    permission_classes = [AllowAny, ]
    search_fields = ['^name', ]
