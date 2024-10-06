import uuid

from django.core.exceptions import ValidationError
from django.db import models


class User(models.Model):
    """Tiktok user model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True, help_text="Should have prefix `@`")
    nickname = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255, unique=True)
    followers = models.PositiveIntegerField(default=0)
    following = models.PositiveIntegerField(default=0)
    visible_content_count = models.PositiveIntegerField(default=0)
    avatar_url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def clean(self):
        if not self.username.startswith("@"):
            raise ValidationError("Username should have prefix `@`")


class TiktokMonitor(models.Model):
    """Monitor specific Tiktok user accounts posts"""

    username = models.CharField(max_length=255, help_text="Should have prefix `@`")
    enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class SavedTiktokVideo(models.Model):
    id = models.CharField(max_length=25, primary_key=True)
    tiktok_user = models.ForeignKey(TiktokMonitor, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
