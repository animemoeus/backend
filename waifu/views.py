import random

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Image
from .serializers import RandomWaifuSerializer, WaifuDetailSerializer, WaifuListSerialzer


@api_view(["GET"])
def index(request):
    if request.method == "GET":
        # waifu count per page
        count = request.query_params.get("count", 20)

        # check NSFW
        nsfw = request.query_params.get("nsfw", False)
        if nsfw and nsfw.lower() == "true":
            nsfw = True
        else:
            nsfw = False

        # NSFW filter
        if nsfw:
            waifu = Image.objects.all().order_by("-id")
        else:
            waifu = Image.objects.filter(
                is_nsfw=False,
            ).order_by("-id")

        paginator = PageNumberPagination()
        paginator.page_size = count  # waifu count per page
        waifu = paginator.paginate_queryset(waifu, request)
        serializer = WaifuListSerialzer(waifu, many=True)

        return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def detail(request, image_id):
    if request.method == "GET":
        try:
            waifu = Image.objects.get(
                image_id=image_id,
            )
            serializer = WaifuDetailSerializer(waifu)
            return Response(serializer.data)
        except Image.DoesNotExist:
            return Response({"detail": "Not found bitch."}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def random_waifu(request):
    # get random waifu from database
    total_records = Image.objects.count()

    if not total_records:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Generate a random index within the range of total_records
    random_index = random.randint(0, total_records - 1)

    # Retrieve a single random record using the generated index
    waifu = Image.objects.order_by("id")[random_index]
    serializer = RandomWaifuSerializer(waifu)
    return Response(serializer.data)
