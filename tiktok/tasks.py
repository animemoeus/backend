from celery import shared_task

from .models import TiktokMonitor
from .utils import TiktokVideoNoWatermark


@shared_task()
def tiktok_user_monitor():
    tiktok_users = TiktokMonitor.objects.filter(enabled=True)

    for user in tiktok_users:
        user = TiktokVideoNoWatermark(user)
        user.save_videos(user.get_feed())
