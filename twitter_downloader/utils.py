import requests
from django.conf import settings


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
    def download_video(cls, tweet_url: str):
        querystring = {
            "url": tweet_url,
            "Cookie": cls.COOKIE,
        }

        response = requests.get(cls.URL, headers=cls.HEADERS, params=querystring)

        try:
            return response.json()
        except ValueError:
            return None
