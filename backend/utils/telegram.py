import hashlib
import hmac
import json
from urllib.parse import unquote

from django.http import HttpRequest


class TelegramWebhookParser:
    def __init__(self, request: HttpRequest):
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
        if data.get("message") and not data.get("message").get("text"):
            return None

        user = data.get("message").get("from")
        message = data.get("message").get("text") or ""

        return {"user": user, "text_message": message}


def validate_telegram_mini_app_data(query_string: str, bot_token: str, constant_str: str = "WebAppData") -> bool:
    """
    Validates the data received from the Telegram web app, using the
    method documented here:
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app

    query_string - the query string passed by the web app
    bot_token - Telegram bot's token
    constant_str - constant string (default = "WebAppData")
    """

    # Parse the query string and extract the hash string
    parsed_data = dict(chunk.split("=") for chunk in unquote(query_string).split("&"))
    received_hash = parsed_data.pop("hash")

    # Sort the remaining parsed data
    sorted_data = sorted(parsed_data.items(), key=lambda x: x[0])
    data_string = "\n".join([f"{key}={value}" for key, value in sorted_data])

    # Generate the secret key using the constant string and bot token
    secret_key = hmac.new(constant_str.encode(), bot_token.encode(), hashlib.sha256).digest()

    # Generate the data check hash using the secret key and sorted data string
    calculated_hash = hmac.new(secret_key, data_string.encode(), hashlib.sha256).hexdigest()

    # Validate the received hash with the calculated hash
    return calculated_hash == received_hash
