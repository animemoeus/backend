import json
from typing import Literal

import requests
from django.db import models


class BaseTelegramUserModel(models.Model):
    class Meta:
        abstract = True

    BOT_TOKEN = None

    user_id = models.CharField(max_length=25)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, default="")
    username = models.CharField(max_length=255, blank=True, default="")

    is_active = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def send_chat_action(self, action: Literal["typing"]) -> None:
        url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendChatAction"
        payload = json.dumps({"chat_id": self.user_id, "action": "typing"})
        headers = {"Content-Type": "application/json"}

        requests.request("POST", url, headers=headers, data=payload)

    def send_message(self, message: str):
        self.send_chat_action("typing")

        url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMessage"
        payload = json.dumps({"chat_id": self.user_id, "text": message})
        headers = {"Content-Type": "application/json"}
        requests.request("POST", url, headers=headers, data=payload)
