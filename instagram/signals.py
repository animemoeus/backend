# signals.py
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from .models import UserFollower, UserFollowing


# User Follower model
# Automatically create profile picture from URL when object saved
@receiver(pre_save, sender=UserFollower)
def user_follower_save_profile_picture_from_url(sender, instance: UserFollowing, **kwargs):
    field_name = "profile_picture"
    file_extension = "jpg"
    file_url = instance.profile_picture_url

    if not instance.profile_picture:
        instance.save_from_url_to_file_field(field_name, file_extension, file_url)


# User Follower model
# Automatically delete file from storage when object deleted
@receiver(pre_delete, sender=UserFollower)
def user_follower_delete_profile_picture(sender, instance, **kwargs):
    if instance.profile_picture:
        instance.profile_picture.delete(save=False)


# User Following model
# Automatically create profile picture from URL when object saved
@receiver(pre_save, sender=UserFollowing)
def user_following_save_profile_picture_from_url(sender, instance: UserFollowing, **kwargs):
    field_name = "profile_picture"
    file_extension = "jpg"
    file_url = instance.profile_picture_url

    if not instance.profile_picture:
        instance.save_from_url_to_file_field(field_name, file_extension, file_url)


# User Following model
# Automatically delete file from storage when object deleted
@receiver(pre_delete, sender=UserFollowing)
def user_following_delete_profile_picture(sender, instance, **kwargs):
    if instance.profile_picture:
        instance.profile_picture.delete(save=False)
