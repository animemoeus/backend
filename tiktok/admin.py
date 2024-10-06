from django.contrib import admin

from .models import SavedTiktokVideo, TiktokMonitor, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = (
        "nickname",
        "user_id",
        "avatar_url",
        "followers",
        "following",
        "visible_content_count",
        "created_at",
        "updated_at",
    )
    list_display = [
        "username",
        "nickname",
        "following",
        "followers",
        "visible_content_count",
        "created_at",
        "updated_at",
    ]
    search_fields = ("username", "nickname")

    fieldsets = (
        (None, {"fields": ("username", "nickname", "avatar_url")}),
        (
            "User Info",
            {"fields": ("user_id", "followers", "following", "visible_content_count")},
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(TiktokMonitor)
class TiktokMonitorAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = ["username", "created_at", "updated_at", "enabled"]
    search_fields = ("username",)


@admin.register(SavedTiktokVideo)
class SavedTiktokVideoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
