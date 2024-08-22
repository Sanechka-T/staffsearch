from users.models import Employer
from django.db import models
from djmoney.models.fields import MoneyField


# Create your models here.
class Vacancy(models.Model):
    company = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='vacancies')
    title = models.CharField(max_length=100, blank=False, verbose_name='Название вакансии')
    profession = models.CharField(max_length=50, blank=False, verbose_name='Профессия')
    field_of_activity = models.CharField(max_length=50, blank=False, verbose_name='Сфера деятельности')
    description = models.TextField(blank=False, verbose_name='Описание вакансии')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d', default=None, blank=True, null=True,
                              verbose_name='Логотип или фотография')
    date_uploaded = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания вакансии')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления вакансии')

    def __str__(self):
        return f"Вакансия {self.title}"

    class Meta:
        verbose_name = "Вакансию"
        verbose_name_plural = "Вакансии"


class Conditions(models.Model):
    EMPLOYMENT_CHOICES = (
        ('full-time', 'Полный день'),
        ('free-work-schedule', 'Свободный'),
        ('shift-work', 'Вахтовый'),
        ('shifts', 'Сменный'),
    )
    CONTRACT_CHOICES = (
        ('employment-contract', 'Трудовой договор'),
        ('GPH-contract-with-sole-proprietor', 'Договор ГПХ с ИП'),
        ('GPH-contract-with-self-employed', 'Договор ГПХ с самозанятым'),
        ('GPH-contract-with-individual', 'Договор ГПХ с физлицом'),
    )
    FREQUENCY_CHOICES = (
        ('every-day', 'Каждый день'),
        ('twice-month', 'Дважды в месяц'),
        ('once-week', 'Раз в неделю'),
        ('once-month', 'Раз в месяц'),
    )
    vacancy = models.OneToOneField('Vacancy', on_delete=models.CASCADE, related_name='conditions')
    employment = models.CharField(max_length=18, choices=EMPLOYMENT_CHOICES, blank=False, default='full-time',
                                  verbose_name='Тип занятости')
    contract = models.CharField(max_length=33, choices=CONTRACT_CHOICES, default='employment-contract',
                                verbose_name='Способ оформления')
    salary = MoneyField(max_digits=14, decimal_places=2, default_currency='RUB', verbose_name='Зарплата')
    underworking = models.BooleanField(default=False, blank=True, verbose_name='Подработка')
    remote_work = models.BooleanField(default=False, verbose_name='Удалённая работа', blank=True)
    frequency_payments = models.CharField(max_length=11, choices=FREQUENCY_CHOICES, default='once-week',
                                          verbose_name='Частота выплат')
    what_employees_get = models.TextField(blank=True, null=True, verbose_name='Что получают работники')

    class Meta:
        verbose_name = "Условие"
        verbose_name_plural = "Условия"

