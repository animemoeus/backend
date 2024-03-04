from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import Settings as TwitterDownloaderSettings
from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "first_name", "last_name", "username", "is_active", "is_banned")
    readonly_fields = ("user_id", "first_name", "last_name", "username", "created_at", "updated_at")


admin.site.register(TwitterDownloaderSettings, SingletonModelAdmin)
