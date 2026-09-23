from django.db import models
from core.models import BaseModel
class Brand(BaseModel):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name