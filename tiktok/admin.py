from django.contrib import admin

from .models import SavedTiktokVideo, TiktokMonitor


@admin.register(TiktokMonitor)
class TiktokMonitorAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = ["username", "created_at", "updated_at", "enabled"]
    search_fields = ("username",)


@admin.register(SavedTiktokVideo)
class SavedTiktokVideoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
