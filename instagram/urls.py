from django.urls import path

from .views import InstagramUserListView, RoastingProfileView

urlpatterns = [
    path("users/", InstagramUserListView.as_view(), name="instagram_user_list"),
    path("roasting/<str:username>/", RoastingProfileView.as_view(), name="roasting"),
]

app_name = "instagram"
