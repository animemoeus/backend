from django.conf import settings
from django.test import TestCase

from backend.utils.telegram import validate_telegram_mini_app_data

# class TestTwitterDownloader(TestCase):
#     def test_download_video(self):
#         print("awokawok")
#         # Mock response
#         mock_response = {"status": "success", "video_url": "https://example.com/video.mp4"}

#         with patch("twitter_downloader.utils.requests.get") as mock_get:
#             mock_get.return_value.json.return_value = mock_response

#             # Create an instance of TwitterDownloader
#             downloader = TwitterDownloader(
#                 "https://example.com/api", {"X-RapidAPI-Key": "key", "X-RapidAPI-Host": "host"}
#             )

#             # Call the download_video method
#             result = downloader.download_video("https://twitter.com/user/status/123456789")

#             # Assert the result
#             self.assertEqual(result, mock_response)


# Suggested code may be subject to a license. Learn more: ~LicenseLog:3939693502.
class TestValidateTelegramMiniAppData(TestCase):
    def test_validate_mini_app_data_true(self):
        telegram_bot_token = settings.TWITTER_VIDEO_DOWNLOADER_BOT_TOKEN
        init_data = "query_id=AAHXv_03AAAAANe__TfVCFD_&user=%7B%22id%22%3A939376599%2C%22first_name%22%3A%22arterrr%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22artertendean%22%2C%22language_code%22%3A%22en%22%2C%22is_premium%22%3Atrue%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1723083100&hash=83dae1980c08b7706c4f572eef937c10f885101eb1f56848203ba88e7cd708ec"

        result = validate_telegram_mini_app_data(init_data, telegram_bot_token)
        self.assertTrue(result)

    def test_validate_mini_app_data_false(self):
        telegram_bot_token = settings.TWITTER_VIDEO_DOWNLOADER_BOT_TOKEN
        init_data = "query_id=AAHXv_03AAAAANe__TfVCFD_&user=%7B%22id%22%3A939376599%2C%22first_name%22%3A%22arterrr%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22artertendean%22%2C%22language_code%22%3A%22en%22%2C%22is_premium%22%3Atrue%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1723083100&hash=83dae1980c08b7706c4f572eef937c10f885101eb1f56848203ba88e7cd708ecinvalid"

        result = validate_telegram_mini_app_data(init_data, telegram_bot_token)
        self.assertFalse(result)
