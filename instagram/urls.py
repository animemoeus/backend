from django.urls import path

from .views import InstagramUserListView

urlpatterns = [
    path("users/", InstagramUserListView.as_view(), name="instagram_user_list"),
]

app_name = "instagram"
