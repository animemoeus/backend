from celery import shared_task

from .models import User as InstagramUser


@shared_task
def get_instagram_users_stories():
    instagram_user = InstagramUser.objects.filter(allow_auto_update_stories=True)

    for user in instagram_user:
        get_instagram_user_stories.delay(user.username)


@shared_task
def get_instagram_user_stories(username: str):
    instagram_user = InstagramUser.objects.get(username=username)
    stories, saved_stories = instagram_user.update_user_stories()

    return f"{len(saved_stories)}/{len(stories)} stories updated"


@shared_task
def update_instagram_users_profile():
    instagram_user = InstagramUser.objects.all()

    for user in instagram_user:
        update_instagram_user_profile.delay(user.username)


@shared_task
def update_instagram_user_profile(username: str):
    instagram_user = InstagramUser.objects.get(username=username)
    instagram_user.update_information_from_api()
