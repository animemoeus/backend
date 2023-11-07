from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import DiscordWebhook, Image


@admin.register(Image)
class ImageAdmin(ImportExportModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = ("image_id",)
    search_fields = ("image_id",)


@admin.register(DiscordWebhook)
class DiscordWebhookAdmin(admin.ModelAdmin):
    pass
