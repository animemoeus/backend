# Generated by Django 4.2.7 on 2024-03-06 16:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("twitter_downloader", "0007_remove_downloadedtweet_id_downloadedtweet_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="downloadedtweet",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]