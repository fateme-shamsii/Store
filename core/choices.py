from django.db import models

class Status(models.IntegerChoices):
    PENDING = 1, "Pending"
    ACCEPTED = 2, "Accepted"
    REJECTED = 3, "Rejected"
    EXPIRED = 4, "Expired"

class StoreStatus(models.IntegerChoices):
    PENDING = 1, "Pending"
    ACCEPTED = 2, "Accepted"
    REJECTED = 3, "Rejected"

class OrderStatus(models.IntegerChoices):
    PENDING = 1, "Pending"
    PAID = 2, "Paid"
    CANCELLED = 3, "Cancelled"


