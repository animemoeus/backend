from rest_framework.serializers import ModelSerializer

from .models import User as InstagramUser
from .models import UserFollower as InstagramUserFollower
from .models import UserFollowing as InstagramUserFollowing


class InstagramUserSerializer(ModelSerializer):
    class Meta:
        model = InstagramUser
        exclude = [
            "profile_picture_url",
        ]


class InstagramUserFollowerSerializer(ModelSerializer):
    class Meta:
        model = InstagramUserFollower
        exclude = ["profile_picture_url", "user"]


class InstagramUserFollowingSerializer(ModelSerializer):
    class Meta:
        model = InstagramUserFollowing
        exclude = ["profile_picture_url", "user"]
