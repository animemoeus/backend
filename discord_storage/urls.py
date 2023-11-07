from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload-from-url/", views.upload_from_url, name="upload-from-url"),
    path("upload-from-file/", views.upload_from_file, name="upload-from-file"),
    path(
        "api/upload-from-url/",
        views.UploadFromURLView.as_view(),
        name="upload-from-url-v1",
    ),
    path(
        "api/upload-from-file/",
        views.UploadFromFileView.as_view(),
        name="upload-from-file-v1",
    ),
]

app_name = "discord_storage"
