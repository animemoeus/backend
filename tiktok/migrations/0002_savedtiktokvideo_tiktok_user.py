# Generated by Django 4.2.7 on 2023-12-20 07:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tiktok", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="savedtiktokvideo",
            name="tiktok_user",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="tiktok.tiktokmonitor"),
        ),
    ]
