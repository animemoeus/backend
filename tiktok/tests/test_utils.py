from django.test import TestCase

from tiktok.utils import TikHubAPI


class TestTikHubAPI(TestCase):
    def setUp(self):
        self.tikhub = TikHubAPI()

    def test__request(self):
        response = self.tikhub.request("/api/v1/tiktok/web/fetch_user_profile?uniqueId=tiktok")
        response_data = response.json().get("data")

        self.assertEqual(response.status_code, 200, "Should return 200 status code")
        self.assertIsNotNone(response_data, "Should not return empty data")

    def test_get_user_id(self):
        user_id = self.tikhub.get_user_id("aangiehsl")
        self.assertEqual(user_id, "MS4wLjABAAAAPJwdzPJKzzNfqLlFTCqh4v8_zODCuUEbH4bNCELzegjPXmvN8pirTKmDo4wUzMVl")

    def test_get_user_info(self):
        user_info = self.tikhub.get_user_info("aangiehsl")
        self.assertEqual(user_info["username"], "arter_tendean",
                         "Should return the correct username")
