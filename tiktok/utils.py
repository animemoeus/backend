import requests
from django.conf import settings
from saiyaku import retry

from .models import SavedTiktokVideo


class TikHubAPI:
    def get_tiktok_user_id(self, username: str) -> str:
        data = self.request(f"/api/v1/tiktok/web/fetch_user_profile?uniqueId={username}")
        return data.get("id")

    @staticmethod
    def request(url: str, method: str = "GET") -> dict:
        base_url = settings.TIKHUB_API_URL
        headers = {"Authorization": f"Bearer {settings.TIKHUB_API_KEY}"}

        response = requests.request(method, f"{base_url}/{url}", headers=headers, timeout=10)
        return response.json()


class TiktokVideoNoWatermark:
    """https://github.com/yi005/Tiktok-Video-No-Watermark"""

    def __init__(self, username: str) -> None:
        self.username = username

    def __str__(self):
        return self.username

    @property
    def posts(self) -> list[dict]:
        # Because of the API limitations, we only get the first page of the feed data.
        # TODO: Use the cursor data to get more information
        url = f"https://www.tikwm.com/api/user/posts?unique_id={self.username}&count=33"
        response = requests.request("GET", url)

        tiktok_videos = response.json().get("data").get("videos")
        return tiktok_videos

    @retry(tries=10, delay=10)
    def get_post_data_once(self):
        url = f"https://www.tikwm.com/api/user/posts?unique_id={self.username}&count=50"
        response = requests.request("GET", url)

        data = response.json().get("data")
        return data

    @retry(tries=10, delay=10)
    def get_post_data_with_cursor(self, cursor=0):
        url = f"https://www.tikwm.com/api/user/posts?unique_id={self.username}&count=50&cursor={cursor}"
        response = requests.request("GET", url)

        data = response.json().get("data")
        return data

    @retry(tries=10, delay=10)
    def get_all_post(self):
        data = self.get_post_data_once()
        cursor = data.get("cursor")
        has_more = data.get("hasMore")
        videos = data.get("videos")

        while has_more:
            data = self.get_post_data_with_cursor(cursor=cursor)
            cursor = data.get("cursor")
            has_more = data.get("hasMore")
            videos += data.get("videos")

            if not has_more:
                break

        return videos[::-1]

    def save_videos(self):
        # Only send video that not sent yet
        for video in self.get_all_post():
            if not SavedTiktokVideo.objects.filter(id=video.get("video_id")).exists():
                SavedTiktokVideo.objects.create(id=video.get("video_id"))
                send_to_private_telegram_channel(video.get("play"), video.get("title"))


@retry(tries=10, delay=1)
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
