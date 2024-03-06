from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import DownloadedTweet
from .models import Settings as TwitterDownloaderSettings
from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "first_name", "last_name", "username", "is_active", "is_banned")
    readonly_fields = ("user_id", "first_name", "last_name", "username", "created_at", "updated_at")


@admin.register(DownloadedTweet)
class DownloadedTweetAdmin(admin.ModelAdmin):
    list_display = ("tweet_url", "telegram_user", "created_at")
    readonly_fields = ("tweet_url", "telegram_user", "created_at")
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False


admin.site.register(TwitterDownloaderSettings, SingletonModelAdmin)
