import time

from celery import shared_task

from .models import TiktokMonitor
from .utils import TiktokVideoNoWatermark


@shared_task()
def tiktok_user_monitor():
    tiktok_users = TiktokMonitor.objects.filter(enabled=True)

    for user in tiktok_users:
        user = TiktokVideoNoWatermark(user)
        user.save_videos(user.get_feed())

        # The API has rate limits, so we need to add delay before the next request
        time.sleep(15)
