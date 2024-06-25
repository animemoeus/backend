from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import DownloadedTweet


@shared_task
def delete_old_data():
    now = timezone.now()
    one_month_ago = now - timedelta(days=30)
    DownloadedTweet.objects.order_by("-created_at").filter(created_at__lt=one_month_ago).delete()
