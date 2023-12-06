import json

from django.http import HttpRequest


class TelegramWebhookParser:
    def __init__(self, request: HttpRequest) -> None | dict:
        self.request = request

    @property
    def data(self):
        try:
            data = json.loads(self.request)
        except Exception:
            return None

        # Reject if not first message (eg. edited or deleted message)
        if not data.get("message"):
            return None

        # Reject if messaage is not text message
        if not data.get("message").get("text"):
            return None

        user = data.get("message").get("from")
        message = data.get("message").get("text") or ""

        return {"user": user, "text_message": message}
