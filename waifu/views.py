import random
import re

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.utils.telegram import TelegramWebhookParser

from .models import Image, TelegramUser
from .pagination import WaifuListPagination
from .serializers import WaifuDetailSerializer, WaifuListSerialzer
from .utils import PixivIllust


class WaifuListView(ListAPIView):
    serializer_class = WaifuListSerialzer
    pagination_class = WaifuListPagination

    def get_queryset(self):
        nsfw = self.request.query_params.get("nsfw")
        queryset = (
            Image.objects.all().order_by("-id")
            if nsfw == "true"
            else Image.objects.filter(is_nsfw=False).order_by("-id")
        )

        return queryset


class WaifuDetailView(RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = WaifuDetailSerializer
    lookup_field = "image_id"


class RandomWaifuView(GenericAPIView):
    serializer_class = WaifuDetailSerializer

    def get_queryset(self):
        # get random waifu from database
        total_records = Image.objects.count()

        # Generate a random index within the range of total_records
        random_index = random.randint(0, total_records - 1)

        # Retrieve a single random record using the generated index
        return Image.objects.order_by("id")[random_index]

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class TelegramUserWebhook(APIView):
    BANNED_ACCOUNT_MESSAGE = "You are banned! ☠️"
    INACTIVE_ACCOUNT_MESSAGE = "Contact admin to activate your account 🚀"

    def post(self, request) -> Response:
        webhook = TelegramWebhookParser(request.body)

        if not webhook.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            telegram_user = TelegramUser.objects.get(user_id=webhook.data.get("user").get("id"))
        except TelegramUser.DoesNotExist:
            telegram_user = TelegramUser.objects.create(
                user_id=webhook.data.get("user").get("id"),
                first_name=webhook.data.get("user").get("first_name"),
                last_name=webhook.data.get("user").get("last_name") or "",
                username=webhook.data.get("user").get("username") or "",
            )

        if telegram_user.is_banned:
            telegram_user.send_message(TelegramUserWebhook.BANNED_ACCOUNT_MESSAGE)
            return Response(TelegramUserWebhook.BANNED_ACCOUNT_MESSAGE)

        if not telegram_user.is_active:
            telegram_user.send_message(TelegramUserWebhook.INACTIVE_ACCOUNT_MESSAGE)
            return Response(TelegramUserWebhook.INACTIVE_ACCOUNT_MESSAGE)

        if webhook.data.get("text_message") == "/start":
            telegram_user.send_message("(～￣▽￣)～")

        if "https://www.pixiv.net/" in webhook.data.get("text_message"):
            url_pattern = re.compile(r"https://www.pixiv.net/\S+")
            message = webhook.data.get("text_message")
            match = url_pattern.search(message)

            if match:
                illust_link = match.group()
            else:
                telegram_user.send_message("Can't get the Pixiv illustation URL from the message 🥲")

            pixiv_illust = PixivIllust(illust_link)
            pixiv_illust.save()
            telegram_user.send_message("Trying to upload...")
        else:
            telegram_user.send_message("Unknown message 🧠")

        return Response()
