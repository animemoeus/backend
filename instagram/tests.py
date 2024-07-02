from django.test import TestCase
from rest_framework import status

from .models import User as InstagramUser


class InstagramTestCase(TestCase):
    def setUp(self):
        self.user_1 = InstagramUser.objects.create(username="arter_tendean")
        self.user_2 = InstagramUser.objects.create(username="retra_naednet")

    def test_get_information_from_api(self):
        status_code_1, user_1_info = self.user_1.get_information_from_api()
        status_code_2, user_2_info = self.user_2.get_information_from_api()

        self.assertEqual(status_code_1, status.HTTP_200_OK)
        self.assertEqual(user_1_info.get("username"), "arter_tendean")

        self.assertEqual(status_code_2, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(user_2_info, {})
