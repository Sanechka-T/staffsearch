# Generated by Django 4.2.13 on 2024-08-06 09:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_additionally_car_additionally_tools_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='date_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления резюме'),
        ),
        migrations.AddField(
            model_name='service',
            name='date_uploaded',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата создания резюме'),
            preserve_default=False,
        ),
    ]
