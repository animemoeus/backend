from rest_framework import serializers

from waifu.models import Image


class WaifuListSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class WaifuDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

    def to_representation(self, instance):
        if "discord" in instance.thumbnail:
            instance.thumbnail = f"https://api.animemoe.us/discord/refresh/?url={instance.thumbnail}"

        if "discord" in instance.original_image:
            instance.original_image = f"https://api.animemoe.us/discord/refresh/?url={instance.original_image}"
        return super().to_representation(instance)


class RandomWaifuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

    def to_representation(self, instance):
        if "discord" in instance.thumbnail:
            instance.thumbnail = f"https://api.animemoe.us/discord/refresh/?url={instance.thumbnail}"

        if "discord" in instance.original_image:
            instance.original_image = f"https://api.animemoe.us/discord/refresh/?url={instance.original_image}"
        return super().to_representation(instance)
