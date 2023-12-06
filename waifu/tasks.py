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
def save_pixiv_illust(illust_data: dict, pyscord_data: dict) -> None:
    Image.objects.create(
        image_id=pyscord_data.get("id"),
        original_image=pyscord_data.get("url"),
        thumbnail=pyscord_data.get("proxy_url"),
        width=pyscord_data.get("width"),
        height=pyscord_data.get("height"),
        creator_name=illust_data.get("creator_name"),
        creator_username=illust_data.get("creator_username"),
        caption=illust_data.get("title"),
        source=illust_data.get("source"),
    )


@shared_task(autoretry_for=(Exception,), max_retries=10, retry_backoff=True)
def update_pixiv_image_url(illust_data: dict, image_url: str) -> None:
    """Change original Pixiv image url to Discord image url"""

    response = pyscord_storage.upload_from_url("animemoeus-waifu.jpg", image_url)
    if response.get("status") != 200:
        raise Exception(response)

    pyscord_data = response.get("data")
    save_pixiv_illust(illust_data, pyscord_data)


@shared_task()
def update_pixiv_image_url_and_save_to_db(illust_data: dict) -> None:
    for image in illust_data.get("images"):
        update_pixiv_image_url.delay(illust_data, image)
