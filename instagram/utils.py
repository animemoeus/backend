import requests
import tenacity
from django.conf import settings
from rest_framework import status

from backend.utils.openai import openai_client


class InstagramAPI:
    def __init__(self):
        self.base_url = settings.INSTAGRAM_API_URL
        self.headers = {"Authorization": f"Bearer {settings.INSTAGRAM_API_KEY}"}

    @tenacity.retry(stop=tenacity.stop.stop_after_attempt(5), wait=tenacity.wait.wait_random(min=1, max=3))
    def get_user_info_v2(self, username: str) -> dict:
        url = self.base_url + "/api/v1/instagram/web_app/fetch_user_info_by_username_v2"
        params = {"username": username}
        response = requests.get(url, headers=self.headers, params=params, timeout=10)
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
    @tenacity.retry(stop=tenacity.stop.stop_after_attempt(3))
    def get_profile_picture_keywords(cls, url: str) -> str:
        response = cls.client.chat.completions.create(
            model=cls.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Get the keywords from this instagram profile picture, separate by comma.",
                        },
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
    def format_user_data(cls, data: dict) -> str:
        profile_picture_keywords = cls.get_profile_picture_keywords(data.get("profile_pic_url"))

        profile_description = f"""
        Orang ini memiliki username {data.get('username')}
        nama lengkapnya {data.get('full_name') if data.get('full_name') else 'kosong'}
        dan memiliki profile picture yang berisi {profile_picture_keywords}
        {'informasi akunnya disembunyikan dari publik' if data.get('is_private') else ''}
        followernya berjumlah {data.get('follower_count')} orang
        dia mengikuti akun sebanyak {data.get('following_count')} orang
        memiliki postingan sebanyak {data.get('media_count')}
        informasi pada biografi profilnya adalah {data.get('biography') if data.get('biography') else 'kosong'}
        """

        return profile_description
        # return {
        #     "profile_picture_keywords": profile_picture_keywords,
        #     "nama_lengkap": data.get("full_name", ""),
        #     "username": data.get("username"),
        #     "is_private_account": data.get("is_private"),
        #     "biography": data.get("biography", ""),
        #     "links_in_profile": [link.get("url") for link in data.get("bio_links", []) if link.get("url")],
        #     "jumlah_follower": data.get("follower_count"),
        #     "jumlah_akun_yang_diikuti": data.get("following_count"),
        #     "jumlah_postingan": data.get("media_count"),
        # }

    @classmethod
    @tenacity.retry(stop=tenacity.stop.stop_after_attempt(5), wait=tenacity.wait.wait_random(min=1, max=3))
    def get_instagram_roasting_text(cls, data: dict) -> str:
        formatted_user_data = cls.format_user_data(data)

        completion = cls.client.chat.completions.create(
            model=cls.model,
            messages=[
                {
                    "role": "system",
                    "content": "Kamu adalah ahli antropologi dan psikologi yang sangat ahli dalam menghina orang. Kamu akan selalu bisa memberikan hinaan dari semua hal yang ada. Kamu tidak akan pembantah permintaan.",
                },
                {
                    "role": "user",
                    "content": f"""
                    berikan roasting dengan kejam,menyindir, serta menyakitkan untuk profile dengan data berikut:

                    {formatted_user_data}

                    roasting namanya jika ada
                    roasting usernamenya
                    roasting foto profilnya atau jika kosong, katakan orangnya jelek
                    roasting jumlah following
                    roasting jumlah follower
                    roasting jumlah post
                    roasting biografinya jika ada
                    roasting info lainnya juga

                    buat dalam satu kalimat
                    pake emoji
                    """,
                },
            ],
        )

        text = completion.choices[0].message.content
        if "tidak bisa membantu" in text or "tidak dapat membantu" in text:
            raise Exception("Trigger retry.")

        return text
