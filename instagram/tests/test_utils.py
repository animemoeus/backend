from django.test import TestCase

from instagram.utils import InstagramAPI, RoastingIG


class TestGetInstagramRoastingText(TestCase):
    def setUp(self):
        self.instagram_api = InstagramAPI()
        self.instagram_user_data = self.instagram_api.get_user_info_v2("angiehsl")

    def test_get_profile_picture_keywords(self):
        profile_picture_keywords = RoastingIG.get_profile_picture_keywords(
            self.instagram_user_data.get("profile_pic_url")
        )
        self.assertIsNotNone(profile_picture_keywords, "Should return profile picture keywords")

    def test_get_instagram_roasting_text(self):
        roasting_text = RoastingIG.get_instagram_roasting_text(self.instagram_user_data)
        self.assertIsNotNone(roasting_text, "Should return roasting text")
