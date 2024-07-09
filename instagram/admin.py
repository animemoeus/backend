from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from rest_framework import status

from .models import Instaloader, Story, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    change_form_template = "instagram/admin_edit_form.html"

    search_fields = ("username",)
    list_display = (
        "username",
        "updated_from_api_datetime",
        "created_at",
        "updated_at",
        "follower_count",
        "following_count",
    )
    readonly_fields = (
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
        code = obj.update_information_from_api()

        if status.is_success(code):
            self.message_user(request, f"({code}): Successfully get information from API")
        else:
            self.message_user(request, f"({code}): Failed to get information from API", level=messages.ERROR)

    def handle_update_user_stories(self, request, obj: User):
        stories, saved_stories = obj.update_user_stories()
        self.message_user(request, f"{len(saved_stories)}/{len(stories)} stories updated")


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("user", "story_id", "created_at", "story_created_at")
    readonly_fields = ["story_id", "created_at", "story_created_at"]
    search_fields = ("user", "story_id")
    ordering = ("-story_created_at",)


@admin.register(Instaloader)
class InstaloaderAdmin(admin.ModelAdmin):
    change_form_template = "instaloader/admin_edit_form.html"

    list_display = ("user", "is_login_success", "last_login_datetime", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at", "last_login_datetime", "is_login_success")
    search_fields = ("user__username", "user__full_name")
    ordering = ("-user__username",)

    fieldsets = (
        (None, {"fields": ("user",)}),
        (None, {"fields": ("session_file",)}),
        (None, {"fields": ("is_login_success", "last_login_datetime")}),
        (None, {"fields": ("created_at", "updated_at")}),
    )

    def response_change(self, request, obj: User):
        if "_test-login" in request.POST:
            self.handle_test_login(request, obj)
            return HttpResponseRedirect(".")

        return super().response_change(request, obj)

    def handle_test_login(self, request, obj: Instaloader):
        login = obj.test_login()

        if login:
            self.message_user(request, "Login Success (˶ᵔ ᵕ ᵔ˶)")
        else:
            self.message_user(request, "Login Failed (╥﹏╥)", level=messages.ERROR)
