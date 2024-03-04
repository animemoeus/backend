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
