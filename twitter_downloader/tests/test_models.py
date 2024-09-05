from django.test import TestCase

from twitter_downloader.models import TelegramUser


class TestTelegramUserModel(TestCase):
    def setUp(self):
        self.telegram_user = TelegramUser.objects.create(
            user_id="939376599", first_name="Arter", last_name="Tendean", username="artertendean"
        )

    def test_send_chat_action(self):
        result = self.telegram_user.send_chat_action("typing")
        self.assertEqual(result, True, "Test send chat action")

    def test_send_message(self):
        result = self.telegram_user.send_message("Test Telegram user model")
        self.assertEqual(result, True)

    def test_send_document(self):
        result = self.telegram_user.send_document(
            "https://avatars.githubusercontent.com/u/9919", caption="Test document caption"
        )
        self.assertEqual(result, True)

    def test_send_maintenance_message(self):
        result = self.telegram_user.send_maintenance_message()
        self.assertEqual(result, True, "Test maintenance message")

    def test_send_banned_message(self):
        result = self.telegram_user.send_banned_message()
        self.assertEqual(result, True, "Test banned message")

    def test_send_photo(self):
        result = self.telegram_user.send_photo(
            {
                "thumbnail": "https://avatars.githubusercontent.com/u/9919",
                "videos": [{"url": "https://avatars.githubusercontent.com/u/9919", "size": 1337}],
            }
        )
        self.assertEqual(result, True, "Test send photo")

    def test_send_video(self):
        result = self.telegram_user.send_video(
            {
                "thumbnail": "https://avatars.githubusercontent.com/u/9919",
                "description": "Test Send Video CI/CD",
                "videos": [{"url": "https://link.testfile.org/aXCg7h", "size": 1337}],
            }
        )

        self.assertEqual(result, True, "Test send video")

    def test_send_big_video(self):
        result = self.telegram_user.send_video(
            {
                "thumbnail": "https://avatars.githubusercontent.com/u/9919",
                "description": "Test Send Big VideoCI/CD",
                "videos": [
                    {
                        "url": "https://link.testfile.org/aYr11v",
                        "size": 1337,
                    }
                ],
            }
        )

        self.assertEqual(result, True, "Test send video with big file size")

    def test_image_with_inline_url(self):
        result = self.telegram_user.send_image_with_inline_keyboard(
            image_url="https://avatars.githubusercontent.com/u/9919",
            inline_text="Arter Tendean",
            inline_url="https://avatars.githubusercontent.com/u/9919",
        )
        self.assertEqual(result, True, "Test send image with inline url")
