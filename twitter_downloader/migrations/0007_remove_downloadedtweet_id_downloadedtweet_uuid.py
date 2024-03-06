# Generated by Django 4.2.7 on 2024-03-06 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("twitter_downloader", "0006_downloadedtweet"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="downloadedtweet",
            name="id",
        ),
        migrations.AddField(
            model_name="downloadedtweet",
            name="uuid",
            field=models.UUIDField(default=1, editable=False, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
