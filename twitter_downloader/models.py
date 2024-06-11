import json
import uuid

import requests
from django.conf import settings
from django.db import models
from django.urls import reverse
from solo.models import SingletonModel

from models.base import BaseTelegramUserModel


class TelegramUser(BaseTelegramUserModel):
    BOT_TOKEN = settings.TWITTER_VIDEO_DOWNLOADER_BOT_TOKEN

    request_count = models.PositiveIntegerField(default=0)

    def send_maintenance_message(self):
        message = "Hello, since the revenue from ads is too low (coz there is no one clicking the ads), I have to shut down this bot to improve the server cost efficiency. \n\nThanks for using this bot ✌️"
        self.send_message(message)

    def send_banned_message(self):
        message = "Sorry, you are banned from using this bot.\n\nPlease contact the bot owner for more information."
        self.send_message(message)

    def send_photo(self, message):
        self.send_chat_action("upload_photo")

        url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendPhoto"
        payload = json.dumps(
            {
                "chat_id": self.user_id,
                "photo": message.get("thumbnail"),
                "text": "arter",
                "parse_mode": "HTML",
                "reply_markup": {
                    "inline_keyboard": [
                        [{"text": f'🔗 {video["size"]}', "url": video["url"]} for video in message.get("videos")],
                    ]
                },
            }
        )
        headers = {"Content-Type": "application/json"}

        requests.request("POST", url, headers=headers, data=payload)

    def send_video(self, tweet_data):
        self.send_chat_action("upload_video")

        url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendVideo"
        payload = json.dumps(
            {
                "chat_id": self.user_id,
                "video": tweet_data.get("videos")[0]["url"],
                "caption": tweet_data.get("description"),
                "parse_mode": "HTML",
                "reply_to_message_id": "",
                "reply_markup": {
                    "inline_keyboard": [
                        [{"text": f'🔗 {video["size"]}', "url": video["url"]} for video in tweet_data.get("videos")],
                    ]
                },
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            self.send_photo(tweet_data)

    def send_image_with_inline_keyboard(
        self,
        image_url: str,
        inline_text: str,
        inline_url: str,
    ):
        url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendPhoto"
        headers = {"Content-Type": "application/json"}

        payload = json.dumps(
            {
                "chat_id": self.user_id,
                "photo": image_url,
                "parse_mode": "HTML",
                "disable_web_page_preview": "True",
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {
                                "text": inline_text,
                                "web_app": {"url": inline_url},
                            }
                        ],
                    ]
                },
            }
        )

        requests.request("POST", url, headers=headers, data=payload)


class DownloadedTweet(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    tweet_url = models.URLField(max_length=255)
    tweet_data = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tweet_url

    def send_to_telegram_user(self):
        url = f'https://api.animemoe.us{reverse("twitter-downloader:safelink")}?key={str(self.uuid)}'
        self.telegram_user.send_image_with_inline_keyboard(self.tweet_data.get("thumbnail"), "Download", url)


class ExternalLink(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    counter = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Settings(SingletonModel):
    class Meta:
        verbose_name = "Twitter Downloader Settings"

    webhook_url = models.URLField(blank=True)

    is_maintenance = models.BooleanField(default=False)

    def __str__(self):
        return "Twitter Downloader Settings"

    def save(self, *args, **kwargs):
        self.set_webhook()
        super().save(*args, **kwargs)

    def set_webhook(self):
        if self.webhook_url:
            url = f"https://api.telegram.org/bot{settings.TWITTER_VIDEO_DOWNLOADER_BOT_TOKEN}/setWebhook?url={self.webhook_url}/"
            requests.request("GET", url)
