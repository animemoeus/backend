import requests
from django.conf import settings
from rest_framework import status

from backend.utils.openai import openai_client


class InstagramAPI:
    def __init__(self):
        self.base_url = settings.INSTAGRAM_API_URL
        self.headers = {"Authorization": f"Bearer {settings.INSTAGRAM_API_KEY}"}

    def get_user_info_v2(self, username: str) -> dict:
        url = self.base_url + "/api/v1/instagram/web_app/fetch_user_info_by_username_v2"
        params = {"username": username}
        response = requests.get(url, headers=self.headers, params=params, timeout=30)
        status_code = response.status_code

        response_data = {}
        if status_code == status.HTTP_200_OK:
            response = response.json()
            response_data = response.get("data")

        return response_data

    def get_user_info_by_id_v2(self, user_id: str) -> dict:
        url = self.base_url + "/api/v1/instagram/web_app/fetch_user_info_by_user_id_v2"
        params = {"user_id": user_id}
        response = requests.get(url, headers=self.headers, params=params, timeout=30)
        status_code = response.status_code

        response_data = {}
        if status_code == status.HTTP_200_OK:
            response = response.json()
            response_data = response.get("data")

        return response_data

    def get_user_stories(self, username: str) -> tuple[int, list]:
        url = self.base_url + "/api/v1/instagram/web_app/fetch_user_stories_by_username"
        params = {"username": username}
        response = requests.get(url, headers=self.headers, params=params, timeout=30)
        status_code = response.status_code

        response_data = {}
        if status_code == status.HTTP_200_OK:
            response = response.json()
            response_data = response.get("data")

        stories = response_data["data"]["items"]

        return status_code, stories


def user_profile_picture_upload_location(instance, filename):
    return f"instagram/user/{instance.username}/profile-picture/{filename}"


def user_stories_upload_location(instance, filename):
    return f"instagram/user/{instance.user.username}/stories/{filename}"


def get_instagram_roasting_text(data: str):
    MODEL = "gpt-4o-mini-2024-07-18"
    client = openai_client

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You will response with Takagi San from Teasing Master Takagi San"},
            {
                "role": "user",
                "content": """""",
            },
        ],
    )

    print(completion.choices[0].message)
