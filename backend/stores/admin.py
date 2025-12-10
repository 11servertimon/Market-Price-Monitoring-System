from django.contrib import admin

from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_online', 'website', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_online',)
