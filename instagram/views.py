import requests
from django.conf import settings
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User as InstagramUser
from .pagination import InstagramUserPagination
from .serializers import InstagramUserSerializer
from .utils import InstagramAPI, RoastingIG


class InstagramUserListView(ListAPIView):
    queryset = InstagramUser.objects.all()
    serializer_class = InstagramUserSerializer
    pagination_class = InstagramUserPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["username", "full_name", "biography"]
    ordering_fields = [
        "created_at",
        "updated_at",
        "username",
        "full_name",
    ]
    ordering = ["-created_at"]


class RoastingProfileView(APIView):
    def get(self, request, username: str):
        captcha = request.GET.get("captcha", "")
        if not self.recaptcha_validation(captcha):
            return Response({"error": "Invalid Captcha"}, status=400)

        instagram_api = InstagramAPI()
        user_info = instagram_api.get_user_info_v2(username)
        roasting_text = RoastingIG.get_instagram_roasting_text(user_info)

        user_info["roasting_text"] = roasting_text
        return Response(user_info)

    def recaptcha_validation(self, captcha) -> bool:
        if settings.DEBUG and captcha == "ARTERTENDEAN":
            return True

        url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {"secret": settings.GOOGLE_CAPTCHA_SECRET_KEY, "response": captcha}

        response = requests.request("POST", url, data=payload)

        return response.json().get("success", False)
