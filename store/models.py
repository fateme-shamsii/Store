from django.db import models
from django.conf import settings
from city.models import City 


class StoreStatus(models.IntegerChoices):
    PENDING = 1, "Pending"
    ACCEPTED = 2, "Accepted"
    REJECTED = 3, "Rejected"


class Store(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='store')
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='stores')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.PositiveSmallIntegerField(
        choices=StoreStatus.choices,
        default=StoreStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name