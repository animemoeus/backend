# Generated by Django 4.2.7 on 2024-03-06 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("twitter_downloader", "0008_alter_downloadedtweet_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="downloadedtweet",
            name="uuid",
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
    ]
