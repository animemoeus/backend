from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random/", views.random_waifu, name="random"),
    path("<str:image_id>/", views.detail, name="detail"),
]

app_name = "waifu"
