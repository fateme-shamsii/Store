from django.db import models
from django.conf import settings
from core.models import SoftDeleteModel

class Profile(SoftDeleteModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=10)
    mobile_phone = models.CharField(max_length=20)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name