# Generated by Django 5.0.6 on 2024-06-27 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Announcement', '0005_paid_announcencer'),
    ]

    operations = [
        migrations.AddField(
            model_name='paid_announcencer',
            name='otp',
            field=models.CharField(default='0000000', max_length=10),
            preserve_default=False,
        ),
    ]
