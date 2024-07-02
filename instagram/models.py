from django.db import models
from django.utils import timezone
from rest_framework import status

from .utils import InstagramAPI


class User(models.Model):
    username = models.CharField(max_length=150, primary_key=True)
    full_name = models.CharField(max_length=150, blank=True)
    profil_picture_url = models.URLField(max_length=500)
    biography = models.TextField(blank=True)

    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

    api_updated_time = models.DateTimeField(default=timezone.now, verbose_name="API Updated Time")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username}"

    def get_information_from_api(self) -> tuple[int, dict]:
        api_client = InstagramAPI()
        status_code, user_info = api_client.get_user_info_v2(self.username)

        if status_code != status.HTTP_200_OK:
            return status_code, {}

        self.api_updated_time = timezone.now()
        self.save()

        return status_code, user_info

    def update_information_from_api(self) -> int:
        status_code, user_info = self.get_information_from_api()

        if status_code != status.HTTP_200_OK:
            return status_code

        if user_info.get("full_name"):
            self.full_name = user_info.get("full_name")

        if user_info.get("biography"):
            self.biography = user_info.get("biography")

        if user_info.get("profile_pic_url"):
            self.profil_picture_url = user_info.get("profile_pic_url")

        if user_info.get("hd_profile_pic_url_info") and user_info.get("hd_profile_pic_url_info").get("url"):
            self.profil_picture_url = user_info.get("hd_profile_pic_url_info").get("url")

        if user_info.get("follower_count"):
            self.follower_count = user_info.get("follower_count")

        if user_info.get("following_count"):
            self.following_count = user_info.get("following_count")

        self.api_updated_time = timezone.now()
        self.save()

        return status_code
