import uuid

import instaloader
import requests
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework import status

from .utils import InstagramAPI, user_profile_picture_upload_location, user_stories_upload_location


class User(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    profile_picture = models.FileField(upload_to=user_profile_picture_upload_location, blank=True, null=True)
    profile_picture_url = models.URLField(max_length=500)
    biography = models.TextField(blank=True)
    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

    updated_from_api_datetime = models.DateTimeField(verbose_name="Update from API datetime", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username}"

    def get_information_from_api(self) -> tuple[int, dict]:
        """
        Get Instagram user information from the API

        Returns:
            tuple[int, dict]: A tuple containing the HTTP status code and the user information.
        """

        api_client = InstagramAPI()
        status_code, user_info = api_client.get_user_info_v2(self.username)

        if status_code != status.HTTP_200_OK:
            return status_code, {}

        return status_code, user_info

    def update_information_from_api(self) -> int:
        status_code, user_info = self.get_information_from_api()
        if status_code != status.HTTP_200_OK:
            return status_code

        if "full_name" in user_info:
            self.full_name = user_info["full_name"]

        if "biography" in user_info:
            self.biography = user_info["biography"]

        if "follower_count" in user_info:
            self.follower_count = user_info["follower_count"]

        if "following_count" in user_info:
            self.following_count = user_info["following_count"]

        if user_info.get("hd_profile_pic_url_info") and user_info.get("hd_profile_pic_url_info").get("url"):
            hd_profile_pic_url = user_info.get("hd_profile_pic_url_info").get("url")

            # Check if the profile picture url is empty and update the file field
            if not self.profile_picture_url:
                self.profile_picture_url = hd_profile_pic_url
                self.save_from_url_to_file_field("profile_picture", "jpg", self.profile_picture_url)

            # Check if the profile picture is empty and update the file field
            if not self.profile_picture and self.profile_picture_url:
                self.save_from_url_to_file_field("profile_picture", "jpg", hd_profile_pic_url)

            # Check if the profile picture URL has changed and update the profile picture field
            if self.profile_picture_url.split("?")[0] != hd_profile_pic_url.split("?")[0]:
                self.save_from_url_to_file_field("profile_picture", "jpg", hd_profile_pic_url)

            self.profile_picture_url = hd_profile_pic_url

        self.updated_from_api_datetime = timezone.now()
        self.save()

        return status_code

    def get_user_stories(self) -> list:
        api_client = InstagramAPI()
        status_code, raw_stories = api_client.get_user_stories(self.username)

        if status_code != status.HTTP_200_OK:
            return

        stories = []
        for story in raw_stories:
            stories.append(
                {
                    "story_id": story.get("id"),
                    "thumbnail_url": story.get("thumbnail_url_original"),
                    "media_url": story.get("video_url_original") or story.get("thumbnail_url_original"),
                    "created_at": story.get("taken_at_date"),
                }
            )

        return stories

    def update_user_stories(self) -> tuple[list, list]:
        stories = self.get_user_stories()
        saved_stories = []
        if not stories:
            return stories, saved_stories

        for story in stories:
            if Story.objects.filter(story_id=story["story_id"]).exists():
                continue
            else:
                x = Story.objects.create(
                    user=self,
                    story_id=story["story_id"],
                    thumbnail_url=story["thumbnail_url"],
                    media_url=story["media_url"],
                    story_created_at=story["created_at"],
                )
                saved_stories.append(x)

        return stories, saved_stories

    def save_from_url_to_file_field(self, field_name: str, file_format: str, file_url: str) -> None:
        response = requests.get(file_url, timeout=30)

        if not response.status_code == status.HTTP_200_OK:
            return

        if hasattr(self, field_name):
            getattr(self, field_name).save(f"{uuid.uuid4()}.{file_format}", ContentFile(response.content))


class Story(models.Model):
    class Meta:
        verbose_name = "Story"
        verbose_name_plural = "Stories"

    story_id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail_url = models.URLField(max_length=1000)
    media_url = models.URLField(max_length=1000, blank=True)

    thumbnail = models.ImageField(upload_to=user_stories_upload_location, blank=True, null=True)
    media = models.FileField(upload_to=user_stories_upload_location, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    story_created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.story_id}"

    def save_from_url_to_file_field(self, field_name: str, file_format: str, file_url: str) -> None:
        response = requests.get(file_url, timeout=30)

        if not response.status_code == status.HTTP_200_OK:
            return

        if hasattr(self, field_name):
            getattr(self, field_name).save(f"{uuid.uuid4()}.{file_format}", ContentFile(response.content))


class Instaloader(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_file = models.FileField(upload_to="instagram/instaloader/sessions/")

    is_login_success = models.BooleanField(default=False)
    last_login_datetime = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}"

    def test_login(self) -> bool:
        self.instaloader = instaloader.Instaloader()

        with self.session_file.file as session_file:
            self.instaloader.context.load_session_from_file(self.user.username, session_file)

        login = self.instaloader.test_login()
        if login:
            self.is_login_success = True
        else:
            self.is_login_success = False

        self.last_login_datetime = timezone.now()
        self.save()

        return bool(login)

    # def get_profile_info(self, username: str):
    #     if not username:
    #         return
    #     if not self.test_login():
    #         return

    #     profile = instaloader.Profile.from_username(self.instaloader.context, username)
    #     return profile

    #     self.instaloader.load_session_from_file(username=self.user.username, filename=self.session_file.path)

    # def get_stories(self):
    #     if not self.test_login():
    #         return

    #     for story in self.instaloader.get_stories():
    #         print(story.url)
    #         print(story.video_url)
    #         break


@receiver(post_save, sender=Story)
def story_post_save(sender, instance, **kwargs):
    # Check if the thumbnail is empty and update the file field
    if not instance.thumbnail:
        instance.save_from_url_to_file_field("thumbnail", "jpg", instance.thumbnail_url)

    # Check if the media is empty and update the file field
    if not instance.media and instance.media_url:
        media_type = instance.media_url.split("?")[0].split(".")[-1]  # Should be jpg or mp4
        instance.save_from_url_to_file_field("media", media_type, instance.media_url)
