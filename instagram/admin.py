from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from rest_framework import status

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    change_form_template = "instagram/admin_edit_form.html"

    search_fields = ("username",)
    list_display = ("username", "api_updated_time", "created_at", "updated_at", "follower_count", "following_count")
    readonly_fields = (
        "full_name",
        "biography",
        "profil_picture_url",
        "follower_count",
        "following_count",
        "api_updated_time",
        "created_at",
        "updated_at",
    )
    ordering = ("username",)

    def response_change(self, request, obj: User):
        if "_update-information-from-api" in request.POST:
            self.handle_update_information_from_api(request, obj)
            return HttpResponseRedirect(".")

        return super().response_change(request, obj)

    def handle_update_information_from_api(self, request, obj: User):
        code = obj.update_information_from_api()

        if status.is_success(code):
            self.message_user(request, f"({code}): Successfully get information from API")
        else:
            self.message_user(request, f"({code}): Failed to get information from API", level=messages.ERROR)
