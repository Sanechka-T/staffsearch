# Generated by Django 4.2.13 on 2024-08-06 09:21

from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_alter_feedback_estimation_alter_photos_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionally',
            name='car',
            field=models.CharField(blank=True, choices=[('yes', 'Есть'), ('no', 'Нет')], default='no', max_length=3, verbose_name='Автомобиль'),
        ),
        migrations.AddField(
            model_name='additionally',
            name='tools',
            field=models.CharField(blank=True, choices=[('yes', 'Да'), ('no', 'Нет')], default='no', max_length=3, verbose_name='Инструменты'),
        ),
        migrations.AlterField(
            model_name='additionally',
            name='contract',
            field=models.CharField(blank=True, choices=[('yes', 'Да'), ('no', 'Нет')], default='no', max_length=3, verbose_name='Контракт'),
        ),
        migrations.AlterField(
            model_name='additionally',
            name='minimum_order',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default_currency='RUB', max_digits=3, null=True, verbose_name='Минимальная сумма заказа'),
        ),
        migrations.AlterField(
            model_name='additionally',
            name='purchase',
            field=models.CharField(blank=True, choices=[('yes', 'Возможна'), ('no', 'Нет')], default='no', max_length=3, verbose_name='Закупка материалов'),
        ),
        migrations.AlterField(
            model_name='additionally',
            name='warranty',
            field=models.CharField(blank=True, choices=[('yes', 'Есть'), ('no', 'Нет')], default='no', max_length=3, verbose_name='Гарантия'),
        ),
    ]
