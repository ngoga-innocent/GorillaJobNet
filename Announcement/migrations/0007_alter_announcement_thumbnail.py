# Generated by Django 5.0.6 on 2024-06-30 22:11

import Announcement.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Announcement', '0006_paid_announcencer_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to=Announcement.models.announcement_thumbnail_path),
        ),
    ]