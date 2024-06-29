# Generated by Django 5.0.6 on 2024-06-25 09:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Announcement', '0003_alter_announcement_announcer_description_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='company_name',
            field=models.CharField(default='Gorilla Job net', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='announcement',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='announcement',
            name='experience',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='announcement',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='announcer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
