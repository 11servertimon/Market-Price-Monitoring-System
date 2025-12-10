from rest_framework import viewsets

from .models import PriceRecord
from .serializers import PriceRecordSerializer


class PriceRecordViewSet(viewsets.ModelViewSet):
    queryset = PriceRecord.objects.select_related('product', 'store').all().order_by('-captured_at')
    serializer_class = PriceRecordSerializer
