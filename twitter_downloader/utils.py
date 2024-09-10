import re

import requests
from django.conf import settings
from saiyaku import retry


class TooManyRequestException(Exception):
    pass


class TwitterDownloader:
    URL = settings.TWITTER_DOWNLOADER_API_URL
    HEADERS = {
        "X-RapidAPI-Key": settings.TWITTER_DOWNLOADER_KEY,
        "X-RapidAPI-Host": settings.TWITTER_DOWNLOADER_HOST,
    }
    COOKIE = settings.TWITTER_DOWNLOADER_COOKIE

    def __init__(self, url, headers):
        self.URL = url
        self.HEADERS = headers

    @classmethod
    @retry(exceptions=TooManyRequestException, delay=1, tries=5)
    def get_video_data(cls, tweet_url: str):
        querystring = {
            "url": tweet_url,
            "Cookie": cls.COOKIE,
        }

        response = requests.get(cls.URL, headers=cls.HEADERS, params=querystring)

        # Raise too many request exception to trigger auto retry
        if response.status_code == 429:
            raise TooManyRequestException

        try:
            response = response.json()
        except ValueError:
            return None

        if not response.get("data"):
            return None

        if response.get("data") and response.get("data")[0].get("type") != "video":
            return None

        _videos = []
        for data in response.get("data")[0].get("video_info"):
            if data.get("bitrate"):
                _videos.append(
                    {
                        "bitrate": data.get("bitrate"),
                        "size": re.findall(r"[0-9]+x[0-9]+", data.get("url"))[0],
                        "url": data.get("url"),
                    }
                )

        _videos = sorted(_videos, key=lambda d: d["bitrate"])[::-1]

        return {
            "id": response.get("id"),
            "thumbnail": response.get("data")[0].get("media"),
            "description": response.get("description") or "",
            "videos": _videos,
        }
