# Generated by Django 4.2.7 on 2024-07-17 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("waifu", "0003_telegramuser"),
    ]

    operations = [
        migrations.AlterField(
            model_name="telegramuser",
            name="user_id",
            field=models.CharField(max_length=25, unique=True),
        ),
    ]