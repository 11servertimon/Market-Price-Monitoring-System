from django.contrib import admin

from .models import PriceRecord


@admin.register(PriceRecord)
class PriceRecordAdmin(admin.ModelAdmin):
    list_display = ('product', 'store', 'price', 'currency', 'captured_at', 'created_at')
    search_fields = ('product__name', 'store__name', 'currency')
    list_filter = ('currency', 'store')
    autocomplete_fields = ('product', 'store')
