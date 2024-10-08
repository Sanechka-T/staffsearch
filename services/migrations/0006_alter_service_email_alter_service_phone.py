# Generated by Django 4.2.13 on 2024-08-06 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_alter_additionally_minimum_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='service',
            name='phone',
            field=models.CharField(max_length=12, verbose_name='Телефон'),
        ),
    ]
