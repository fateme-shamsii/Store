from celery import shared_task
from django.utils import timezone

from .models import Advertisement, AdvertisementStatus


@shared_task
def expire_old_advertisements():
    expired_count = Advertisement.objects.filter(
        expires_at__lte=timezone.now(),
        status__in=[
            AdvertisementStatus.PENDING,
            AdvertisementStatus.ACCEPTED,
        ],
    ).update(
        status=AdvertisementStatus.EXPIRED,
    )

    return expired_count