from celery import shared_task

from .models import User as InstagramUser


@shared_task
def get_users_stories():
    instagram_user = InstagramUser.objects.all()

    for user in instagram_user:
        get_user_stories.delay(user.username)


@shared_task
def get_user_stories(username: str):
    instagram_user = InstagramUser.objects.get(username=username)
    instagram_user.update_user_stories()


@shared_task
def update_users_profile():
    instagram_user = InstagramUser.objects.all()

    for user in instagram_user:
        update_user_profile.delay(user.username)


@shared_task
def update_user_profile(username: str):
    instagram_user = InstagramUser.objects.get(username=username)
    instagram_user.update_information_from_api()
