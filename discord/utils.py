import json

import requests
from django.conf import settings


class DiscordAPI:
    def __init__(self, url: str) -> None:
        self.url = url

    @classmethod
    def refresh_url(self, url: str) -> str:
        payload = json.dumps({"attachment_urls": [url]})

        headers = {
            "Authorization": f"Bot {settings.DISCORD_REFRESH_URL_BOT_TOKEN}",
            "Content-Type": "application/json",
        }

        response = requests.request("POST", settings.DISCORD_REFRESH_URL, headers=headers, data=payload)

        return response.json().get("refreshed_urls")[0].get("refreshed")
