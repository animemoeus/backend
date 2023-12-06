import random

from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from .models import Image
from .pagination import WaifuListPagination
from .serializers import WaifuDetailSerializer, WaifuListSerialzer


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
