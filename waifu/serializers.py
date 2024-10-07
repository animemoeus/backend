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


class RandomWaifuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
