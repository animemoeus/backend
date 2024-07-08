from rest_framework import filters
from rest_framework.generics import ListAPIView

from .models import User as InstagramUser
from .pagination import InstagramUserPagination
from .serializers import InstagramUserSerializer


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
