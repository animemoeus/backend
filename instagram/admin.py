from django.contrib import admin, messages
from django.http import HttpResponseRedirect

from .models import RoastingLog, Story, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    change_form_template = "instagram/admin_edit_form.html"

    filter_horizontal = ["follower", "following"]

    search_fields = ("username",)
    list_display = (
        "username",
        "updated_from_api_datetime",
        "allow_auto_update_stories",
        "created_at",
        "updated_at",
        "follower_count",
        "following_count",
    )
    readonly_fields = (
        "instagram_id",
        "full_name",
        "biography",
        "profile_picture_url",
        "follower_count",
        "following_count",
        "updated_from_api_datetime",
        "created_at",
        "updated_at",
    )
    ordering = ("username",)

    def response_change(self, request, obj: User):
        if "_update-information-from-api" in request.POST:
            self.handle_update_information_from_api(request, obj)
            return HttpResponseRedirect(".")

        if "_update-stories-from-api" in request.POST:
            self.handle_update_user_stories(request, obj)
            return HttpResponseRedirect(".")

        return super().response_change(request, obj)

    def handle_update_information_from_api(self, request, obj: User):
        try:
            obj.update_information_from_api()
            self.message_user(request, "Successfully get information from API")
        except Exception as e:
            self.message_user(request, "Failed to get information from the API", level=messages.ERROR)
            self.message_user(request, e, level=messages.ERROR)

    def handle_update_user_stories(self, request, obj: User):
        stories, saved_stories = obj.update_user_stories()
        self.message_user(request, f"{len(saved_stories)}/{len(stories)} stories updated")


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("user", "story_id", "created_at", "story_created_at")
    readonly_fields = ["story_id", "created_at", "story_created_at"]
    search_fields = ("user", "story_id")
    ordering = ("-story_created_at",)


@admin.register(RoastingLog)
class RoastingLogAdmin(admin.ModelAdmin):
    list_display = ("username", "created_at")
    readonly_fields = ("username", "roasting_text", "user_data", "created_at")
    search_fields = ("username",)
    ordering = ("-created_at",)
