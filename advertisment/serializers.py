from rest_framework import serializers
from .models import Advertisement
from store.models import StoreStatus
from django.utils import timezone

class AdvertisementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = (
            'id',
            'brand',
            'category',
            'store',
            'title',
            'description',
            'price',
            'status',
            'total_quantity',
            'expires_at',
        )
        read_only_fields = (
            'id',
            'status',
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than zero"
            )
        return value
    
    def validate_expires_at(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                "Expiration date must be in the future."
            )
        return value

    def validate_total_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Total quantity must be greater than zero"
            )
        return value  
       
    def validate(self, attrs):
        request = self.context.get('request')
        store = attrs.get('store')
        brand = attrs.get('brand')
        category = attrs.get('category')

        if not store.is_active:
            raise serializers.ValidationError(
                "Selected Store is not active."
            )

        if brand and store.status != StoreStatus.ACCEPTED:
            raise serializers.ValidationError("user can't buy the brand")

        if brand and not brand.is_active:
            raise serializers.ValidationError(
                "Selected brand is not active."
            )
        
        if category and not category.is_active:
            raise serializers.ValidationError(
                "Selected category is not active."
            )

        if store.owner != request.user:
            raise serializers.ValidationError(
                "You can only create advertisements for your own store."
            )
        return attrs
        

class AdvertisementListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)
    brand_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    available_quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Advertisement
        fields = (
            'id',
            'title',
            'description',
            'price',
            'store',
            'store_name',
            'category',
            'category_name',
            'brand',
            'brand_name',
            'status',
            'status_display',
            'total_quantity',
            'hold_quantity',
            'available_quantity',
            'expires_at',
        )


    def get_brand_name(self, obj):
        if obj.brand:
            return obj.brand.name
        return None


        