from django.urls import path

from .views import SafelinkView, TelegramWebhookView

urlpatterns = [
    path("safelink/", SafelinkView.as_view(), name="safelink"),
    path("telegram-webhook/", TelegramWebhookView.as_view(), name="telegram-webhook"),
]

app_name = "twitter_downloader"
