from django.test import TestCase

from twitter_downloader.models import TelegramUser


class TestTelegramUserModel(TestCase):
    def setUp(self):
        self.telegram_user = TelegramUser.objects.create(
            user_id="939376599", first_name="Arter", last_name="Tendean", username="artertendean"
        )

    def test_send_chat_action(self):
        result = self.telegram_user.send_chat_action("typing")
        self.assertEqual(result, True)

    def test_send_message(self):
        result = self.telegram_user.send_message("Test Telegram User Model")
        self.assertEqual(result, True)

    def test_send_document(self):
        result = self.telegram_user.send_document(
            "https://avatars.githubusercontent.com/u/9919", caption="Test Document Caption"
        )
        self.assertEqual(result, True)
