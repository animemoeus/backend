from django.contrib import admin, messages
from django.http import HttpResponseRedirect

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
        if "_get-information-from-api" in request.POST:
            self.handle_get_information_from_api(request, obj)
            return HttpResponseRedirect(".")

        return super().response_change(request, obj)

    def handle_get_information_from_api(self, request, obj: User):
        result = obj.get_information_from_api()

        if result:
            self.message_user(request, "Successfully get information from API")
        else:
            self.message_user(request, "Failed to get information from API", level=messages.ERROR)
