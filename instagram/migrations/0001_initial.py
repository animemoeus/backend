# Generated by Django 4.2.7 on 2024-07-05 05:19

from django.db import migrations, models
import django.db.models.deletion
import instagram.utils
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=150)),
                ("full_name", models.CharField(blank=True, max_length=150)),
                (
                    "profile_picture",
                    models.FileField(
                        blank=True, null=True, upload_to=instagram.utils.user_profile_picture_upload_location
                    ),
                ),
                ("profile_picture_url", models.URLField(max_length=500)),
                ("biography", models.TextField(blank=True)),
                ("follower_count", models.PositiveIntegerField(default=0)),
                ("following_count", models.PositiveIntegerField(default=0)),
                ("api_updated_time", models.DateTimeField(blank=True, null=True, verbose_name="API Updated Time")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Story",
            fields=[
                ("story_id", models.CharField(max_length=50, primary_key=True, serialize=False)),
                ("thumbnail_url", models.URLField(max_length=1000)),
                ("media_url", models.URLField(blank=True, max_length=1000)),
                (
                    "thumbnail",
                    models.ImageField(blank=True, null=True, upload_to=instagram.utils.user_stories_upload_location),
                ),
                (
                    "media",
                    models.FileField(blank=True, null=True, upload_to=instagram.utils.user_stories_upload_location),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("story_created_at", models.DateTimeField()),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="instagram.user")),
            ],
            options={
                "verbose_name": "Story",
                "verbose_name_plural": "Stories",
            },
        ),
    ]
