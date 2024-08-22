from django.contrib.auth.models import User
from django.db import models

# Create your models here.
"""if request.user.employer подключить блок профиля компании, иначе обычный профиль"""


class Employer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, unique=True, db_index=True, related_name='employer')
    company_name = models.CharField(max_length=100, verbose_name='Название компании')
    company_description = models.TextField(verbose_name='Описание компании')
    company_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон компании')
    company_email = models.EmailField(blank=True, null=True, verbose_name='Email компании')
    company_address = models.CharField(max_length=200, blank=True, null=True, verbose_name='Адрес компании')
    company_site = models.URLField(blank=True, null=True, verbose_name='Сайт компании')

    class Meta:
        verbose_name = "Работодателя"
        verbose_name_plural = "Работодатели"
