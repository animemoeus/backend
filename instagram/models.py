import uuid

import requests
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone
from rest_framework import status

from .utils import InstagramAPI, user_profile_picture_upload_location


class User(models.Model):
    username = models.CharField(max_length=150, primary_key=True)
    full_name = models.CharField(max_length=150, blank=True)
    profile_picture = models.FileField(upload_to=user_profile_picture_upload_location, blank=True, null=True)
    profile_picture_url = models.URLField(max_length=500)
    biography = models.TextField(blank=True)

    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

    api_updated_time = models.DateTimeField(verbose_name="API Updated Time", blank=True, null=True)

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

        if user_info.get("hd_profile_pic_url_info") and user_info.get("hd_profile_pic_url_info").get("url"):
            hd_profile_pic_url = user_info.get("hd_profile_pic_url_info").get("url")

            # Check if the profile picture URL is empty and update the file field
            if not self.profile_picture_url:
                self.profile_picture_url = hd_profile_pic_url
                self.save_from_url_to_file_field("profile_picture", "jpg", self.profile_picture_url)

            # Check if the profile picture URL is not empty and update the file field
            if not self.profile_picture and self.profile_picture_url:
                self.save_from_url_to_file_field("profile_picture", "jpg", hd_profile_pic_url)

            # Check if the profile picture URL has changed and update the file field
            if self.profile_picture_url.split("?")[0] != hd_profile_pic_url.split("?")[0]:
                self.save_from_url_to_file_field("profile_picture", "jpg", hd_profile_pic_url)

            self.profile_picture_url = hd_profile_pic_url

        if user_info.get("follower_count"):
            self.follower_count = user_info.get("follower_count")

        if user_info.get("following_count"):
            self.following_count = user_info.get("following_count")

        self.api_updated_time = timezone.now()
        self.save()

        return status_code

    def save_from_url_to_file_field(self, field_name: str, file_format: str, file_url: str) -> None:
        response = requests.get(file_url, timeout=30)

        if not response.status_code == status.HTTP_200_OK:
            return

        if hasattr(self, field_name):
            getattr(self, field_name).save(f"{uuid.uuid4()}.{file_format}", ContentFile(response.content))
