from rest_framework import viewsets

from .models import Store
from .serializers import StoreSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all().order_by('name')
    serializer_class = StoreSerializer
