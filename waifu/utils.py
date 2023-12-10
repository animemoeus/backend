from typing import Any

from django.conf import settings
from pixivpy3 import AppPixivAPI

from .tasks import update_pixiv_image_url_and_save_to_db


class PixivIllust:
    IllustDetail = Any

    def __init__(self, illust_link: str) -> None:
        self.__illust_link = illust_link
        self.__api = AppPixivAPI()
        self.__api.auth(refresh_token=settings.PIXIVPY_3_REFRESH_TOKEN)

    @property
    def illust_detail(self) -> IllustDetail:
        """Return a dictionary that contains information about pixiv illustraion details"""

        illust_id = self.__illust_link.split("/")[-1]
        json_result = self.__api.illust_detail(illust_id)
        json_result = json_result.get("illust")

        # handle multiple images
        if json_result.get("meta_pages"):
            images = [image.get("image_urls").get("original") for image in json_result.get("meta_pages")]

        # handle single image
        if json_result.get("meta_single_page"):
            images = [
                json_result.get("meta_single_page").get("original_image_url"),
            ]

        formated_result = {
            "creator_name": json_result.get("user").get("name"),
            "creator_username": json_result.get("user").get("account"),
            "title": json_result.get("title"),
            "images": images,
            "source": self.__illust_link,
        }

        return formated_result

    def save(self) -> None:
        update_pixiv_image_url_and_save_to_db.delay(self.illust_detail)
