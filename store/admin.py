from django.contrib import admin

from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'city', 'status', 'is_active', 'created_at',)
    list_filter = ('status', 'is_active', 'city',)
    search_fields = ('name', 'owner__username', 'city__name',)