# Generated by Django 4.2.13 on 2024-08-11 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0003_alter_conditions_vacancy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conditions',
            name='photo',
        ),
        migrations.AddField(
            model_name='vacancy',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photo/%Y/%m/%d', verbose_name='Логотип или фотография'),
        ),
    ]
