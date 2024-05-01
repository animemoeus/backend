from django.shortcuts import redirect
from ninja import NinjaAPI

from .utils import DiscordAPI

api = NinjaAPI()


@api.get("")
def hello(request, url: str):
    refreshed_url = DiscordAPI.refresh_url(url)

    if refreshed_url:
        return redirect(refreshed_url)
    else:
        return redirect("https://github.com/animemoeus/backend")
