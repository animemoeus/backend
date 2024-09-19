# from django.test import Client, TestCase, override_settings
# from django.urls import reverse
# from rest_framework import status

# from waifu.views import TelegramUserWebhook

# from .models import Image, TelegramUser
# from .utils import PixivIllust


# class WaifuTestCase(TestCase):
#     def setUp(self):
#         self.image_1 = Image.objects.create(
#             image_id="123456789",
#             original_image="https://cdn.discordapp.com/attachments/858938620425404426/1015081259497701416/waifu-animemoeus.webp",
#             thumbnail="https://cdn.discordapp.com/attachments/858938620425404426/1015081259497701416/waifu-animemoeus.webp",
#         )
#         Image.objects.create(
#             image_id="12345678910",
#             original_image="https://cdn.discordapp.com/attachments/858938620425404426/1015081259497701416/waifu-animemoeus.webp",
#             thumbnail="https://cdn.discordapp.com/attachments/858938620425404426/1015081259497701416/waifu-animemoeus.webp",
#         )
#         Image.objects.create(
#             image_id="1234567890111",
#             original_image="https://cdn.discordapp.com/attachments/858938620425404426/1015081259497701416/waifu-animemoeus.webp",
#             thumbnail="https://cdn.discordapp.com/attachments/858938620425404426/1015081259497701416/waifu-animemoeus.webp",
#         )

#     def test_get_image_query(self):
#         waifu = Image.objects.count()
#         self.assertEqual(waifu, 3)

#     def test_index_view(self):
#         url = reverse("waifu:index")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.json().get("results")), 3)

#     def test_detail_view(self):
#         # this test should success return http 200 status code
#         url = reverse("waifu:detail", kwargs={"image_id": self.image_1.image_id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # this test should fail and return http 404 status code
#         url = reverse("waifu:detail", kwargs={"image_id": "12345"})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_random_waifu_view(self):
#         url = reverse("waifu:random")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class TestPixivIllust(TestCase):
#     def setUp(self) -> None:
#         self.single_illust = PixivIllust("https://www.pixiv.net/en/artworks/112996839")
#         self.multiple_illust = PixivIllust("https://www.pixiv.net/en/artworks/60795514")

#         self.dummy_illust_data = {
#             "creator_name": "depoo",
#             "creator_username": "depoo",
#             "title": "ハロウィン～高木さん＆（元）高木さん～",
#             "images": ["https://i.pximg.net/img-original/img/2023/10/31/06/19/43/112996839_p0.png"],
#             "source": "https://www.pixiv.net/en/artworks/112996839",
#         }
#         self.dummy_pixiv_image_url = "https://i.pximg.net/img-original/img/2023/10/31/06/19/43/112996839_p0.png"

#     def test_get_single_illust(self):
#         data = self.single_illust.illust_detail
#         self.assertEqual(type(data), dict)
#         self.assertEqual(len(data.get("images")), 1)

#     def test_get_multiple_illust(self):
#         data = self.multiple_illust.illust_detail
#         self.assertEqual(type(data), dict)
#         self.assertEqual(len(data.get("images")), 9)

#     @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
#     def test_save_single_illust(self):
#         self.single_illust.save()
#         self.assertEqual(Image.objects.all().count(), 1)

#     @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
#     def test_save_multiple_illust(self):
#         self.multiple_illust.save()
#         self.assertEqual(Image.objects.all().count(), 9)


# class TestWaifuTelegramWebhook(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.start_webhook_payload = {
#             "update_id": 188954841,
#             "message": {
#                 "message_id": 6415,
#                 "from": {
#                     "id": 939376599,
#                     "is_bot": "false",
#                     "first_name": "Arter",
#                     "last_name": "Tendean",
#                     "username": "artertendean",
#                     "language_code": "en",
#                 },
#                 "chat": {
#                     "id": 939376599,
#                     "first_name": "Arter",
#                     "last_name": "Tendean",
#                     "username": "artertendean",
#                     "type": "private",
#                 },
#                 "date": 1701879994,
#                 "text": "/start",
#                 "entities": [{"offset": 0, "length": 6, "type": "bot_command"}],
#             },
#         }

#     def test_start_webhook(self):
#         url = reverse("waifu:telegram-webhook")
#         response = self.client.post(path=url, data=self.start_webhook_payload, content_type="application/json")

#         self.assertEqual(response.status_code, 200, "The new telegram user should be created")
#         self.assertEqual(TelegramUser.objects.all().count(), 1, "The new user should be in the database")
#         self.assertEqual(
#             response.data, TelegramUserWebhook.INACTIVE_ACCOUNT_MESSAGE, "The new creator should be inactive"
#         )
