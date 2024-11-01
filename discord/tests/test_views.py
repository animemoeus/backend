import requests
from django.test import TestCase


class TestDiscordRefreshURL(TestCase):
    def setUp(self):
        self.expired_url = (
            "https://cdn.discordapp.com/attachments/858938620425404426/1248453128991412224/animemoeus-waifu.jpg"
        )
        self.invalid_url = "https://google.com"

    def test_refresh_expired_url(self):
        # request using the default URL
        response = requests.get(self.expired_url)
        self.assertEqual(response.status_code, 404)

        # request using the refresher API
        response = self.client.get(f"/discord/refresh/?url={self.expired_url}")
        print(response.status_code)
        self.assertEqual(response.status_code, 302)

        # request using the new url from refershed API
        response = requests.get(response.url)
        self.assertEqual(response.status_code, 200)

    def test_refresh_invalid_url(self):
        response = self.client.get(f"/discord/refresh/?url={self.invalid_url}")
        self.assertEqual(response.status_code, 444)
