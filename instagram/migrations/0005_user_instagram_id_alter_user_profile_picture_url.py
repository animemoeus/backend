# Generated by Django 4.2.7 on 2024-07-17 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("instagram", "0004_instaloader_is_login_success_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="instagram_id",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="profile_picture_url",
            field=models.URLField(help_text="The original profile picture URL from Instagram", max_length=500),
        ),
    ]