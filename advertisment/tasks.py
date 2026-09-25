from celery import shared_task
from django.utils import timezone

from .models import Advertisement
from core.choices import Status


@shared_task
def expire_old_advertisements():
    expired_count = Advertisement.objects.filter(
        expires_at__lte=timezone.now(),
        status__in=[Status.PENDING, Status.ACCEPTED,
        ],
    ).update(status=Status.EXPIRED,)

    return expired_count