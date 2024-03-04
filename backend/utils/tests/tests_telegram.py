from unittest.mock import MagicMock

from backend.utils.telegram import TelegramWebhookParser


def test_telegram_webhook_parser():
    # Create a mock HttpRequest object
    request = MagicMock()

    # Set the request JSON data
    request.json = {
        "message": {
            "from": {
                "id": 123456789,
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
            },
            "text": "Hello, world!",
        }
    }

    # Create an instance of TelegramWebhookParser
    parser = TelegramWebhookParser(request)

    # Test the data property
    assert parser.data == {
        "user": {
            "id": 123456789,
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
        },
        "text_message": "Hello, world!",
    }
