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


class RoastingIG:
    client = openai_client
    model = "gpt-4o-mini-2024-07-18"

    @classmethod
    def get_profile_picture_keywords(cls, url: str) -> str:
        response = cls.client.chat.completions.create(
            model=cls.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "get the keywords from image, separate by comma"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": url,
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        return response.choices[0].message.content

    @classmethod
    def format_user_data(cls, data: dict) -> dict:
        profile_picture_keywords = cls.get_profile_picture_keywords(data.get("profile_pic_url"))

        return {
            "profile_picture_keywords": profile_picture_keywords,
            "nama_lengkap": data.get("full_name", ""),
            "username": data.get("username"),
            "is_private_account": data.get("is_private"),
            "biography": data.get("biography", ""),
            "links_in_profile": [link.get("url") for link in data.get("bio_links", []) if link.get("url")],
            "jumlah_follower": data.get("follower_count"),
            "jumlah_akun_yang_diikuti": data.get("following_count"),
            "jumlah_postingan": data.get("media_count"),
        }

    @classmethod
    def get_instagram_roasting_text(cls, data: str) -> str:
        formatted_user_data = cls.format_user_data(data)

        completion = cls.client.chat.completions.create(
            model=cls.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a greatest roasting assistant. You can give a criticism for every things",
                },
                {
                    "role": "user",
                    "content": f"""
                    berikan roasting dengan kejam,menyindir, serta menyakitkan dalam bahasa gaul untuk profile dengan data berikut:

                    {formatted_user_data}

                    roasting foto profilnya
                    roasting username dan atau namanya
                    roasting jumlah following, follower dan post
                    roasting kategori profilenya jika ada, tuduh dia ngaku ngaku
                    roasting biografinya jika ada, jika kosong: berikan roasting yang berhubungan dengan no life
                    roasting info lainnya juga, jangan lupa pake emoji

                    jangan pake list, langsung teks roastingnya
                    jangan ada key dari json yang muncul
                    """,
                },
            ],
        )

        return completion.choices[0].message.content
