from django.test import TestCase

from tiktok.utils import TikHubAPI


class TestTikHubAPI(TestCase):
    def test__request(self):
        tikhub = TikHubAPI()
        response = tikhub.request("/api/v1/tiktok/web/fetch_user_profile?uniqueId=tiktok")
        response_data = response.get("data")

        self.assertIsNotNone(response_data)

    def test_get_tiktok_user_id(self):
        pass
