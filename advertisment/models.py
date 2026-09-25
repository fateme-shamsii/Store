from django.db import models
from django.db.models import F, Q

from brand.models import Brand
from category.models import Category
from core.models import SoftDeleteModel
from core.choices import Status
from store.models import Store



class Advertisement(SoftDeleteModel):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='advertisements', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='advertisements')
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='advertisements')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.PositiveBigIntegerField()
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.PENDING,)
    total_quantity = models.PositiveIntegerField()
    hold_quantity = models.PositiveIntegerField(default=0)
    expires_at = models.DateTimeField()

    class Meta:
        constraints = [
            models.CheckConstraint(condition=Q(price__gt=0), name='advertisement_price_gt_0'),
            models.CheckConstraint(condition=Q(total_quantity__gt=0), name='advertisement_total_quantity_gt_0'),
            models.CheckConstraint(condition=Q(hold_quantity__gte=0), name='advertisement_hold_quantity_gte_0'),
            models.CheckConstraint(
                condition=Q(total_quantity__gte=F('hold_quantity')),
                name='advertisement_total_quantity_gte_hold_quantity',
            ),
        ]
    def __str__(self):
        return self.title

    @property
    def available_quantity(self):
        return self.total_quantity - self.hold_quantity