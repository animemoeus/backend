import requests
from django.conf import settings
from rest_framework import status


class InstagramAPI:
    BASE_URL = settings.INSTAGRAM_API_URL
    HEADERS = {"Authorization": f"Bearer {settings.INSTAGRAM_API_KEY}"}

    client = requests.Session()
    client.headers.update(HEADERS)

    def __init__(self):
        pass

    @classmethod
    def get_user_info_v2(cls, username: str) -> dict | None:
        url = f"{cls.BASE_URL}/api/v1/instagram/web_app/fetch_user_info_by_username_v2"
        params = {"username": username}
        response = cls.client.get(url, params=params, timeout=30)

        response_data = None
        if response.status_code == status.HTTP_200_OK:
            response = response.json()
            response_data = response.get("data")

        return response_data
