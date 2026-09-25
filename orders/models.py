from django.conf import settings
from django.db import models
from django.db.models import Q

from advertisment.models import Advertisement
from core.models import BaseModel
from core.choices import OrderStatus


class Order(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders',)
    status = models.PositiveSmallIntegerField(choices=OrderStatus.choices, default=OrderStatus.PENDING,)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0,)

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(total_price__gte=0), name='order_total_price_gte_0',),
        ]

    def __str__(self):
        return f"Order #{self.id} - {self.user}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items',)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.PROTECT, related_name='order_items',)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2,)
    total_price = models.DecimalField(max_digits=12, decimal_places=2,)

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(quantity__gt=0), name='order_item_quantity_gt_0',),
            models.CheckConstraint(check=Q(unit_price__gt=0), name='order_item_unit_price_gt_0',),
            models.CheckConstraint(check=Q(total_price__gt=0), name='order_item_total_price_gt_0',),
        ]

    def __str__(self):
        return f"{self.quantity} x {self.advertisement}"