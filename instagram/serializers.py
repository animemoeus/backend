from rest_framework.serializers import ModelSerializer

from .models import User as InstagramUser


class InstagramUserSerializer(ModelSerializer):
    class Meta:
        model = InstagramUser
        exclude = [
            "profile_picture_url",
        ]
