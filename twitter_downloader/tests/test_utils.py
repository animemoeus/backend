# from unittest.mock import patch

# from django.test import TestCase

# from twitter_downloader.utils import TwitterDownloader


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
