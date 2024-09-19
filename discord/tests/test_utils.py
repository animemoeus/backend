import requests
from django.test import TestCase
from rest_framework import status

from discord.utils import DiscordAPI


class TestDiscordAPI(TestCase):
    def setUp(self):
        self.discord_file_url_1 = (
            "https://cdn.discordapp.com/attachments/858938620425404426/1248453128991412224/animemoeus-waifu.jpg"
        )

    def test_failed_refresh_url(self):
        response = requests.get(self.discord_file_url_1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, "Should return 404")
        self.assertEqual(response.text, "This content is no longer available.")

    def test_refresh_url(self):
        result = DiscordAPI.refresh_url(self.discord_file_url_1)
        response = requests.get(result)

        self.assertEqual(response.status_code, status.HTTP_200_OK, "Should return 200 OK")
