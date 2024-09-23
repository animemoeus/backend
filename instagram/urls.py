from django.urls import path

from .views import GetUserInfo, InstagramUserListView

urlpatterns = [
    path("users/", InstagramUserListView.as_view(), name="instagram_user_list"),
    path("get-user-info/<str:username>/", GetUserInfo.as_view(), name="get-user-info"),
]

app_name = "instagram"
