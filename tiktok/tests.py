from django.test import TestCase

from .utils import TiktokVideoNoWatermark, send_to_private_telegram_channel


class TestGetTiktokUserFeed(TestCase):
    def setUp(self):
        self.tiktok_user = TiktokVideoNoWatermark("@aangiehsl")

    def test_get_posts(self):
        self.assertEqual(type(self.tiktok_user.posts), list, "The user feed should be a list")
        self.assertNotEqual(len(self.tiktok_user.posts), 0, "The user feed should be not empty")

    def test_save_video(self):
        self.assertEqual(self.tiktok_user.save_videos([]), False, "Saving empty videos should return False")
        self.assertEqual(
            self.tiktok_user.save_videos(self.tiktok_user.posts[:3]), True, "Saving videos should return True"
        )

    def test_send_video_to_telegram_channel(self):
        self.assertEqual(
            send_to_private_telegram_channel(
                "https://cdn.discordapp.com/attachments/858938620425404426/1180895032111267991/twittervid.com_Crunchyroll_5a93b2.mp4",
                "test caption",
            ),
            200,
        )
