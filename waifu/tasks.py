import random

import pyscord_storage
from celery import shared_task

from .models import DiscordWebhook, Image


@shared_task()
def send_waifu():
    webhooks = DiscordWebhook.objects.filter(is_enabled=True)

    # get random waifu from database
    total_records = Image.objects.count()
    random_index = random.randint(0, total_records - 1)
    waifu = Image.objects.order_by("id")[random_index]

    for webhook in webhooks:
        webhook.send_image(waifu.original_image, waifu.is_nsfw, waifu.creator_name)


@shared_task()
def save_pixiv_illust_to_model(illust_data: dict) -> None:
    """This function will save the Pixiv illust data to model after converting the image url using pyscord_storage."""

    for image in illust_data.get("images"):
        response = pyscord_storage.upload_from_url("animemoeus-waifu.jpg", image)

        if response.get("status") == 200:
            response_data = response.get("data")

            Image.objects.create(
                image_id=response_data.get("id"),
                original_image=response_data.get("url"),
                thumbnail=response_data.get("proxy_url"),
                width=response_data.get("width"),
                height=response_data.get("height"),
                creator_name=illust_data.get("creator_name"),
                creator_username=illust_data.get("creator_username"),
                caption=illust_data.get("title"),
                source=illust_data.get("source"),
            )
