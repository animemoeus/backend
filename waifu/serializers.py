from rest_framework import serializers

from waifu.models import Image


class WaifuListSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            "id",
            "image_id",
            "thumbnail",
            "is_nsfw",
            "creator_name",
            "creator_username",
            "width",
            "height",
        ]


class WaifuDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            "id",
            "image_id",
            "original_image",
            "thumbnail",
            "is_nsfw",
            "creator_name",
            "creator_username",
            "caption",
            "source",
            "width",
            "height",
        ]


class RandomWaifuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            "id",
            "image_id",
            "original_image",
            "thumbnail",
            "is_nsfw",
            "creator_name",
            "creator_username",
            "caption",
            "source",
            "width",
            "height",
        )
