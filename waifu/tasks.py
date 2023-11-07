import random

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
