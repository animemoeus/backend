import json

import requests
from django.conf import settings
from django.db import models
from solo.models import SingletonModel

from models.base import BaseTelegramUserModel


class TelegramUser(BaseTelegramUserModel):
    BOT_TOKEN = settings.TWITTER_VIDEO_DOWNLOADER_BOT_TOKEN

    def send_maintenance_message(self):
        message = "Sorry, the bot is currently under maintenance.\n\nPlease try again later."
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


class DownloadedTweet(models.Model):
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    tweet_url = models.URLField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tweet_url


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
