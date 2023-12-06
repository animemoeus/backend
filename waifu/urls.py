from django.urls import path

from .views import RandomWaifuView, WaifuDetailView, WaifuListView

urlpatterns = [
    path("", WaifuListView.as_view(), name="index"),
    path("random/", RandomWaifuView.as_view(), name="random"),
    path("<str:image_id>/", WaifuDetailView.as_view(), name="detail"),
]

app_name = "waifu"
