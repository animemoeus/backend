from django.urls import path

from .views import (
    InstagramUserDetailView,
    InstagramUserFollowerListView,
    InstagramUserFollowingListView,
    InstagramUserListView,
    RoastingProfileView,
)

urlpatterns = [
    path("users/", InstagramUserListView.as_view(), name="instagram_user_list"),
    path("users/<str:username>/", InstagramUserDetailView.as_view(), name="instagram-user-detail"),
    path(
        "users/<str:username>/follower/", InstagramUserFollowerListView.as_view(), name="instagram-user-follower-list"
    ),
    path(
        "users/<str:username>/following/",
        InstagramUserFollowingListView.as_view(),
        name="instagram-user-following-list",
    ),
    path("roasting/<str:username>/", RoastingProfileView.as_view(), name="roasting"),
]

app_name = "instagram"
