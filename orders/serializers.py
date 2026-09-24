from rest_framework import serializers

from advertisment.models import Advertisement
from .models import Order, OrderItem


class OrderItemCreateSerializer(serializers.Serializer):
    advertisement = serializers.PrimaryKeyRelatedField(
        queryset=Advertisement.objects.all()
    )

    quantity = serializers.IntegerField(
        min_value=1
    )


class CreateOrderSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(
        many=True
    )

    def validate_items(self, value):

        if not value:
            raise serializers.ValidationError(
                "Order must have at least one item."
            )

        advertisement_ids = [
            item['advertisement'].id
            for item in value
        ]

        if len(advertisement_ids) != len(set(advertisement_ids)):
            raise serializers.ValidationError(
                "Duplicate advertisements are not allowed in one order."
            )

        return value


class OrderItemSerializer(serializers.ModelSerializer):

    advertisement_title = serializers.CharField(
        source='advertisement.title',
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'advertisement_title',
            'quantity',
            'unit_price',
            'total_price',
        )


class OrderSerializer(serializers.ModelSerializer):

    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True,
    )

    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = (
            'id',
            'status',
            'status_display',
            'total_price',
            'items',
            'created_at',
        )