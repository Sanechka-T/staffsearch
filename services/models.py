from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField


# Create your models here.
class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=50, verbose_name='Название услуги')
    EXPERIENCE_CHOICES = (
        ('without-experience', 'Без опыта'),
        ('less-than-year', 'Менее года'),
        ('1', '1 год'),
        ('2', '2 года'),
        ('3', '3 года'),
        ('4', '4 года'),
        ('5', '5 лет'),
        ('6', '6 лет'),
        ('7', '7 лет'),
        ('8', '8 лет'),
        ('9', '9 лет'),
        ('10', '10 лет'),
        ('more-than-10', 'Более 10 лет'),
    )
    GROUP_CHOICES = (
        ('1', '1 человек'),
        ('2-4', '2-4 человека'),
        ('5-10', '5-10 человек'),
        ('11-20', '11-20 человек'),
        ('20+', 'от 20 человек'),
    )
    experience = models.CharField(max_length=18, choices=EXPERIENCE_CHOICES, verbose_name='Опыт работы')
    group = models.CharField(max_length=18, choices=GROUP_CHOICES, default='1', verbose_name='Состав группы')
    description = models.TextField(verbose_name='Описание услуги', blank=False)
    price_list = models.TextField(verbose_name='Прайс-лист', blank=True, null=True)
    cost = MoneyField(max_digits=10, decimal_places=2, default_currency='RUB', verbose_name='Стоимость основной услуги')
    phone = models.CharField(max_length=12, verbose_name='Телефон', blank=False)
    email = models.EmailField(max_length=100, verbose_name='Электронная почта', blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания резюме')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления резюме')

    def __str__(self):
        return f"Услуга {self.name} {self.cost}"


class Photos(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photo/resume_images/%Y/%m/%d', verbose_name='Фотографии', blank=True,
                              null=True)


class Feedback(models.Model):
    ESTIMATION_CHOICES = (
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звезд'),
    )
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='feedback')
    estimation = models.IntegerField( choices=ESTIMATION_CHOICES, default=5, verbose_name='Оценка')
    feedback_text = models.TextField(verbose_name='Отзыв', blank=False)


class Additionally(models.Model):
    CONTRACT_CHOICES = (
        ('yes', 'Да'),
        ('no', 'Нет'),
    )
    WARRANTY_CHOICES = (
        ('yes', 'Есть'),
        ('no', 'Нет'),
    )
    PURCHASE_CHOICES = (
        ('yes', 'Возможна'),
        ('no', 'Нет'),
    )
    service = models.OneToOneField('Service', on_delete=models.CASCADE, related_name='additionally')
    contract = models.CharField(max_length=3, choices=CONTRACT_CHOICES, default='no', verbose_name='Контракт',
                                blank=True)
    warranty = models.CharField(max_length=3, choices=WARRANTY_CHOICES, default='no', verbose_name='Гарантия',
                                blank=True)
    minimum_order = MoneyField(max_digits=10, decimal_places=2, default_currency='RUB',
                               verbose_name='Минимальная сумма заказа', blank=True, null=True)
    purchase = models.CharField(max_length=3, choices=PURCHASE_CHOICES, default='no',
                                verbose_name='Закупка материалов', blank=True)
    car = models.CharField(max_length=3, choices=WARRANTY_CHOICES, default='no', verbose_name='Автомобиль',
                           blank=True)
    tools = models.CharField(max_length=3, choices=CONTRACT_CHOICES, default='no', verbose_name='Инструменты',
                             blank=True)
