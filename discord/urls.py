from django.urls import path

from . import views
from .ninja import api as ninja

urlpatterns = [
    path("", views.index, name="index"),
    path("refresh/", ninja.urls, name="refresh"),
]


app_name = "discord"
