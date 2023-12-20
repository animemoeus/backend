from django.db import models


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
