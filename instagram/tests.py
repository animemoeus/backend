from django.test import TestCase

from .models import User as InstagramUser


class InstagramTestCase(TestCase):
    def setUp(self):
        self.user_1 = InstagramUser.objects.create(username="arter_tendean")
        self.user_2 = InstagramUser.objects.create(username="retra_naednet")

    def test_get_information_from_api(self):
        user_1_info = self.user_1.get_information_from_api()
        user_2_info = self.user_2.get_information_from_api()

        self.assertEqual(user_1_info.username, "arter_tendean")
        self.assertEqual(user_2_info, None)
