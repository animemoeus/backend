from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import Image
from .utils import PixivIllust


class WaifuTestCase(TestCase):
    def setUp(self):
        self.image_1 = Image.objects.create(
            image_id="123456789",
            original_image="https://cdn.discordapp.com/attachments/858938620425404426/1015081259497701416/waifu-animemoeus.webp",
            thumbnail="https://cdn.discordapp.com/attachments/858938620425404426/1015081259497701416/waifu-animemoeus.webp",
        )
        Image.objects.create(
            image_id="12345678910",
            original_image="https://cdn.discordapp.com/attachments/858938620425404426/1015081259497701416/waifu-animemoeus.webp",
            thumbnail="https://cdn.discordapp.com/attachments/858938620425404426/1015081259497701416/waifu-animemoeus.webp",
        )
        Image.objects.create(
            image_id="1234567890111",
            original_image="https://cdn.discordapp.com/attachments/858938620425404426/1015081259497701416/waifu-animemoeus.webp",
            thumbnail="https://cdn.discordapp.com/attachments/858938620425404426/1015081259497701416/waifu-animemoeus.webp",
        )

    def test_get_image_query(self):
        waifu = Image.objects.count()
        self.assertEqual(waifu, 3)

    def test_index_view(self):
        url = reverse("waifu:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("results")), 3)

    def test_detail_view(self):
        # this test should success return http 200 status code
        url = reverse("waifu:detail", kwargs={"image_id": self.image_1.image_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # this test should fail and return http 404 status code
        url = reverse("waifu:detail", kwargs={"image_id": "12345"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_random_waifu_view(self):
        url = reverse("waifu:random")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPixivIllust(TestCase):
    def setUp(self) -> None:
        self.single_illust = PixivIllust("https://www.pixiv.net/en/artworks/112996839")
        self.multiple_illust = PixivIllust('PixivIllust("https://www.pixiv.net/en/artworks/60795514')

    def test_get_single_illust(self):
        data = self.single_illust.illust_detail
        self.assertEqual(type(data), dict)
        self.assertEqual(len(data.get("images")), 1)

    def test_get_multiple_illust(self):
        data = self.multiple_illust.illust_detail
        self.assertEqual(type(data), dict)
        self.assertEqual(len(data.get("images")), 9)
