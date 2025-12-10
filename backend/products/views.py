from django.db.models import Avg, Count, Max, Min, OuterRef, Subquery
from django.utils.dateparse import parse_date
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from pricing.models import PriceRecord
from stores.models import Store
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer

    def _filtered_price_records(self, product, request):
        records = PriceRecord.objects.filter(product=product)
        from_date = parse_date(request.query_params.get('from'))
        if from_date:
            records = records.filter(captured_at__date__gte=from_date)

        to_date = parse_date(request.query_params.get('to'))
        if to_date:
            records = records.filter(captured_at__date__lte=to_date)

        return records

    @action(detail=True, methods=['get'], url_path='statistics')
    def statistics(self, request, pk=None):
        product = self.get_object()
        records = self._filtered_price_records(product, request)

        stats = records.aggregate(
            min_price=Min('price'),
            max_price=Max('price'),
            avg_price=Avg('price'),
            num_records=Count('id'),
        )

        latest_record = records.order_by('-captured_at').first()

        data = {
            'min_price': stats['min_price'],
            'max_price': stats['max_price'],
            'avg_price': stats['avg_price'],
            'latest_price': latest_record.price if latest_record else None,
            'currency': latest_record.currency if latest_record else None,
            'num_records': stats['num_records'] or 0,
        }

        return Response(data)

    @action(detail=True, methods=['get'], url_path='price-history')
    def price_history(self, request, pk=None):
        product = self.get_object()
        records = (
            PriceRecord.objects.filter(product=product)
            .select_related('store')
            .order_by('captured_at')
        )

        data = [
            {
                'store_id': record.store_id,
                'store_name': record.store.name,
                'price': record.price,
                'currency': record.currency,
                'captured_at': record.captured_at,
            }
            for record in records
        ]

        return Response(data)

    @action(detail=True, methods=['get'], url_path='store-comparison')
    def store_comparison(self, request, pk=None):
        product = self.get_object()

        latest_price_subquery = (
            PriceRecord.objects.filter(product=product, store=OuterRef('pk'))
            .order_by('-captured_at')
            .values('price')[:1]
        )
        latest_currency_subquery = (
            PriceRecord.objects.filter(product=product, store=OuterRef('pk'))
            .order_by('-captured_at')
            .values('currency')[:1]
        )
        latest_captured_subquery = (
            PriceRecord.objects.filter(product=product, store=OuterRef('pk'))
            .order_by('-captured_at')
            .values('captured_at')[:1]
        )

        stores_with_prices = (
            Store.objects.filter(price_records__product=product)
            .distinct()
            .annotate(
                latest_price=Subquery(latest_price_subquery),
                latest_currency=Subquery(latest_currency_subquery),
                latest_captured_at=Subquery(latest_captured_subquery),
            )
        )

        comparisons = [
            {
                'store_id': store.id,
                'store_name': store.name,
                'price': store.latest_price,
                'currency': store.latest_currency,
                'captured_at': store.latest_captured_at,
            }
            for store in stores_with_prices
            if store.latest_price is not None
        ]

        cheapest_store = None
        most_expensive_store = None

        if comparisons:
            cheapest_store = min(comparisons, key=lambda item: item['price'])
            most_expensive_store = max(comparisons, key=lambda item: item['price'])

        data = {
            'stores': comparisons,
            'cheapest_store': cheapest_store,
            'most_expensive_store': most_expensive_store,
        }

        return Response(data)
