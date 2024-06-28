from django.db import models
from django.utils import timezone

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

    def get_information_from_api(self):
        user_info = InstagramAPI.get_user_info_v2(self.username)

        if not user_info:
            return

        if "full_name" in user_info:
            self.full_name = user_info["full_name"]

        if "profile_pic_url" in user_info:
            self.profil_picture_url = user_info["profile_pic_url"]

        if "hd_profile_pic_url_info" in user_info:
            temp = user_info["hd_profile_pic_url_info"]

            if "url" in temp:
                self.profil_picture_url = temp["url"]

        if "biography" in user_info:
            self.biography = user_info["biography"]

        if "follower_count" in user_info:
            self.follower_count = user_info["follower_count"]

        if "following_count" in user_info:
            self.following_count = user_info["following_count"]

        self.api_updated_time = timezone.now()
        self.save()

        return self
