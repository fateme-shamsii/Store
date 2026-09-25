from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from advertisment.models import Advertisement
from core.choices import Status
from .models import Order, OrderItem

class OrderService:

    @staticmethod
    @transaction.atomic()
    def create_order(*, user, items):
        order = Order.objects.create(
            user=user,
            total_price=0
        )
        order_total_price = 0

        for item in items:
            requested_advertisement = item['advertisement']
            quantity = item['quantity']

            advertisement = Advertisement.objects.select_for_update().get(
                id=requested_advertisement.id,
            )

            OrderService.validate_advertisement_for_order(
                advertisement=advertisement,
                quantity=quantity,
            )

            unit_price = advertisement.price

            order_item = OrderService.create_order_item(
                order=order,
                advertisement=advertisement,
                quantity=quantity,
                unit_price=unit_price,
            )

            advertisement.hold_quantity += quantity
            advertisement.save(update_fields=['hold_quantity'])

        order_total_price += order_item.total_price

        order.total_price = order_total_price
        order.save(update_fields=['total_price'])

        return order


    @staticmethod    
    def create_order_item(*, order, advertisement, quantity, unit_price):
        item_total_price = unit_price * quantity
        order_item = OrderItem.objects.create(
            order=order,
            advertisement=advertisement,
            quantity=quantity,
            unit_price=unit_price,
            total_price=item_total_price
        )
        return order_item

    
    @staticmethod
    def validate_advertisement_for_order(*, advertisement, quantity):
        if advertisement.status != Status.ACCEPTED:
            raise ValidationError(
                "Advertisement is not available for ordering."
            )

        if advertisement.expires_at <= timezone.now():
            raise ValidationError(
                "Advertisement is expired."
            )

        if advertisement.available_quantity < quantity:
            raise ValidationError(
                "Not enough inventory for this advertisement."
            )