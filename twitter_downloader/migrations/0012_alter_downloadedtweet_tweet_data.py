# Generated by Django 4.2.7 on 2024-03-06 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("twitter_downloader", "0011_downloadedtweet_tweet_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="downloadedtweet",
            name="tweet_data",
            field=models.JSONField(default=dict),
        ),
    ]
