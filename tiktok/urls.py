from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]

app_name = "tiktok"
