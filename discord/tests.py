import requests
from django.test import TestCase
from django.urls import reverse


class DiscordTestCase(TestCase):
    def setUp(self):
        self.expired_url = (
            "https://cdn.discordapp.com/attachments/858938620425404426/1248453128991412224/animemoeus-waifu.jpg"
        )

    def test_refresh_expired_url(self):
        # request using the default URL
        response = requests.get(self.expired_url)
        self.assertEqual(response.status_code, 404)

        # request using the refresher API
        response = self.client.get(f"/discord/refresh/?url={self.expired_url}")
        self.assertEqual(response.status_code, 302)

        # request using the new url from refershed API
        response = requests.get(response.url)
        self.assertEqual(response.status_code, 200)
