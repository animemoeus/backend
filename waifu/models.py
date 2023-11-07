from django.db import models


class Image(models.Model):
    image_id = models.CharField(max_length=50)
    original_image = models.CharField(max_length=500, blank=True)
    thumbnail = models.CharField(max_length=500, blank=True)

    is_nsfw = models.BooleanField(default=False)

    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    creator_name = models.CharField(max_length=255, blank=True, default="")
    creator_username = models.CharField(max_length=255, blank=True, default="")
    caption = models.TextField(blank=True, default="")
    source = models.CharField(max_length=255, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.image_id}"
