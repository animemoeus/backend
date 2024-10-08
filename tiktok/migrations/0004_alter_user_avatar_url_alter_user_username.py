# Generated by Django 4.2.14 on 2024-10-06 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tiktok", "0003_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar_url",
            field=models.URLField(max_length=555),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
