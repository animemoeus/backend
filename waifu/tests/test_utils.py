from django.test import TestCase

from waifu.utils import refresh_expired_urls


class TestRefreshExpiredURLS(TestCase):
    def setUp(self):
        self.expired_urls_1 = [
            "https://64.media.tumblr.com/3a7de325951453a7a3ad41ea992d2c4c/5920cbbca6af3345-51/s1280x1920/365844bab8106ae227d1503cb003980c4cb7ef68.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1275631907933261897/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1275631722272260148/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1275631652307075165/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1275631496677298217/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1275631492734783579/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1275631444743426079/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1275631263373590539/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1275631260349235283/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1275631208495321088/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1275630951610716161/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1275630850230190262/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1270956343318151188/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1270956079114747999/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1270955995539046520/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1270955850701471835/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1268536242601988117/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1268536194275344434/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1268536157218668638/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1268536102961020988/animemoeus-waifu.jpg",
            "https://cdn.discordapp.com/attachments/858938620425404426/1268536085483356193/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1275631907933261897/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1275631722272260148/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1275631652307075165/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1275631496677298217/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1275631492734783579/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1275631444743426079/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1275631263373590539/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1275631260349235283/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1275631208495321088/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1275630951610716161/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1275630850230190262/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1270956343318151188/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1270956079114747999/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1270955995539046520/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1270955850701471835/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1268536242601988117/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1268536194275344434/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1268536157218668638/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1268536102961020988/animemoeus-waifu.jpg",
            "https://media.discordapp.net/attachments/858938620425404426/1268536085483356193/animemoeus-waifu.jpg",
        ]

    def test_refresh_expired_urls(self):
        refreshed_urls = refresh_expired_urls(self.expired_urls_1)
        self.assertEqual(len(refreshed_urls), 40)