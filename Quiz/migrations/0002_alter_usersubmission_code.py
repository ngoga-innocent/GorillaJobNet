# Generated by Django 4.2.6 on 2024-06-08 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Payment', '0003_payment_type_subscription_otp'),
        ('Quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubmission',
            name='code',
            field=models.ForeignKey(default='b8287861-aea3-48a3-89b0-8fbd9a8a27cf', on_delete=django.db.models.deletion.CASCADE, to='Payment.otp'),
        ),
    ]
