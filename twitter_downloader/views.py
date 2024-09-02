import re

from django.shortcuts import render
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.utils.telegram import TelegramWebhookParser

from .models import DownloadedTweet
from .models import Settings as TwitterDownloaderSettings
from .models import TelegramUser
from .serializers import ValidateTelegramMiniAppDataSerializer
from .utils import TwitterDownloader


class SafelinkView(View):
    # This decorator is used to allow the iframe to load the page (from Telegram app)
    @xframe_options_exempt
    def get(self, request):
        uuid = request.GET.get("key", None)

        return render(request, "twitter_downloader/download.html", context={"uuid": uuid})

    def post(self, request):
        uuid = request.POST.get("uuid")

        tweet = DownloadedTweet.objects.get(uuid=uuid)
        tweet.telegram_user.send_video(tweet.tweet_data)

        return render(request, "twitter_downloader/success.html")


class TelegramWebhookView(APIView):
    def post(self, request):
        webhook = TelegramWebhookParser(request.body)
        if not webhook.data:
            return Response()

        # Get or create TelegramUser
        user_data = webhook.data.get("user")
        telegram_user, _ = TelegramUser.objects.get_or_create(
            user_id=user_data.get("id"),
            defaults={
                "first_name": user_data.get("first_name"),
                "last_name": user_data.get("last_name") or "",
                "username": user_data.get("username") or "",
            },
        )

        # Update TelegramUser data
        telegram_user.is_active = True
        telegram_user.first_name = user_data.get("first_name")
        telegram_user.last_name = user_data.get("last_name") or ""
        telegram_user.username = user_data.get("username") or ""
        telegram_user.request_count += 1
        telegram_user.save()

        # Check if the bot is under maintenance
        if self.is_maintenance:
            telegram_user.send_maintenance_message()
            return Response()

        if telegram_user.is_banned:
            telegram_user.send_banned_message()
            return Response()

        text_message = webhook.data.get("text_message")
        if text_message:
            self.handle_text_message(telegram_user, text_message)

        return Response()

    @property
    def is_maintenance(self):
        return TwitterDownloaderSettings.get_solo().is_maintenance

    def handle_text_message(self, telegram_user: TelegramUser, message: str):
        # Handle /start command
        if message.lower().startswith("/start"):
            self.handle_start_command(telegram_user)

        # Handle /contact command
        elif message.lower().startswith("/contact"):
            self.handle_contact_command(telegram_user)

        # Handle /about command
        elif message.lower().startswith("/about"):
            self.handle_about_command(telegram_user)

        # Handle tweet link
        elif "https://x.com" in message.lower() or "https://twitter.com" in message.lower():
            telegram_user.send_chat_action("typing")
            self.handle_tweet_link(telegram_user, message)

        # Handle other messages
        else:
            self.handle_other_messages(telegram_user)

    def handle_start_command(self, telegram_user):
        telegram_user.send_message("Welcome to Twitter Video Downloader Bot!\n\no(*￣▽￣*)ブ")
        telegram_user.send_message("Send me a tweet link and I will send you the video and download link!")

    def handle_contact_command(self, telegram_user):
        telegram_user.send_message("Please contact me at arter@animemoe.us for any inquiries.")

    def handle_about_command(self, telegram_user):
        about_message = "This is the Twitter Video Downloader Bot.\n\n"
        about_message += "It allows you to download videos from Twitter by sending a tweet link.\n\n"
        about_message += "Developed by Arter Tendean.\n\n"
        about_message += "For more information, visit our website at https://animemoe.us"
        telegram_user.send_message(about_message)

    def handle_tweet_link(self, telegram_user, message):
        # Extract all strings starting with "https"
        urls = re.findall(r"https://\S+", message.lower())
        url = urls[0] if urls else None

        tweet_data = TwitterDownloader.get_video_data(url)
        if not tweet_data:
            telegram_user.send_message("Sorry, I can't find any video in that tweet link.")
            return Response()

        downloaded_tweet = DownloadedTweet.objects.create(
            tweet_url=message,
            telegram_user=telegram_user,
            tweet_data=tweet_data,
        )
        downloaded_tweet.send_to_telegram_user()

    def handle_other_messages(self, telegram_user):
        telegram_user.send_message(
            "Haha, I'm just a bot.\n\nI can't understand everything.\n\nTry sending a different command!"
        )


class TelegramWebhookV2View(APIView):
    def post(self, request):
        telegram_webhook = TelegramWebhookParser(request.body)

        try:
            webhook_user = telegram_webhook.get_user()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        print(webhook_user)
        return Response("arter tendean")


class ValidateTelegramMiniAppDataView(GenericAPIView):
    serializer_class = ValidateTelegramMiniAppDataSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(status=status.HTTP_200_OK)
