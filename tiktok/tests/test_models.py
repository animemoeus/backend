from django.test import TestCase

from tiktok.models import User as TikTokUser


class TestTikTokUser(TestCase):
    def setUp(self):
        self.user = TikTokUser.objects.create(username="arter_tendean")

    def test_update_data_from_api(self):
        self.user.update_data_from_api()
        self.assertNotEqual(self.user.user_id, "")
        self.assertNotEqual(self.user.avatar_url, "")
