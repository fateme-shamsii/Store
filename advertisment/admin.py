from django.contrib import admin

from .models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'store', 'brand', 'category', 'price', 'status', 'expires_at', 'created_at',)
    list_filter = ('status', 'brand', 'category', 'store',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at', 'hold_quantity', 'available_quantity',)
    search_fields = ('title', 'store__name', 'brand__name', 'category__name',)