import requests
from django.conf import settings

from .models import SavedTiktokVideo


class TiktokVideoNoWatermark:
    """https://github.com/yi005/Tiktok-Video-No-Watermark"""

    def __init__(self, username: str) -> None:
        url = f"https://www.tikwm.com/api/user/info?unique_id={username}"
        response = requests.request("GET", url)

        self.username = response.json().get("data").get("user").get("uniqueId")

    def __str__(self):
        return self.username

    def get_feed(self) -> list[dict]:
        # Because of the API limitations, we only get the first page of the feed data.
        # TODO: Use the cursor data to get more information
        url = f"https://www.tikwm.com/api/user/posts?unique_id={self.username}&count=33"

        response = requests.request("GET", url)
        print(response.status_code)
        print(response.text)
        if response.status_code != 200:
            return

        tiktok_videos = response.json().get("data").get("videos")
        return tiktok_videos

    def save_videos(self, videos: list[dict]) -> bool:
        if not videos:
            return False

        # Only send video that not sent yet
        for video in videos[::-1]:
            if not SavedTiktokVideo.objects.filter(id=video.get("video_id")).exists():
                SavedTiktokVideo.objects.create(id=video.get("video_id"))
                send_to_private_telegram_channel(video.get("play"), video.get("title"))

        return True


def send_to_private_telegram_channel(video_url: str, caption: str = "") -> None:
    """Sent to private Telegram channel by via Telegram Bot"""

    url = f"https://api.telegram.org/bot{settings.TIKTOK_MONITOR_TELEGRAM_BOT_SECRET}/sendDocument"

    payload = {
        "chat_id": settings.TIKTOK_MONITOR_TELEGRAM_PRIVATE_CHANNEL_ID,
        "document": video_url,
        "caption": caption,
        "disable_notification": True,
    }

    response = requests.request("POST", url, data=payload)
    return response.status_code
