from rest_framework import filters
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User as InstagramUser
from .pagination import InstagramUserPagination
from .serializers import InstagramUserSerializer
from .utils import InstagramAPI


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


class GetUserInfo(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, username: str):
        instagram_api = InstagramAPI()
        user_info = instagram_api.get_user_info_v2(username)
        return Response(user_info)
