# Generated by Django 4.2.7 on 2024-03-03 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("twitter_downloader", "0003_rename_twitterdownloadersetting_twitterdownloadersettings"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="twitterdownloadersettings",
            options={"verbose_name": "Twitter Downloader Settings"},
        ),
        migrations.AddField(
            model_name="twitterdownloadersettings",
            name="webhook_url",
            field=models.URLField(blank=True),
        ),
    ]
