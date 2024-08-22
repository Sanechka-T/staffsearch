from django.db import models


# Create your models here.
class Ticket(models.Model):
    TICKET_CHOICES = (
        ('looking-job', 'Ищу работу'),
        ('resume-analysis', 'Анализ резюме'),
        ('work-students', 'Работа для студентов'),
        ('deleting-account', 'Удаление аккаунта'),
        ('other', 'Другое'),
    )
    title = models.CharField(max_length=16, choices=TICKET_CHOICES, verbose_name='Тема обращения', blank=False)
    phone = models.CharField(max_length=12, verbose_name='Телефон', blank=False)
    email = models.EmailField(max_length=100, verbose_name='Электронная почта', blank=False)
    description = models.TextField(verbose_name='Обязанности', blank=False)
    ticket_file = models.FileField(upload_to='ticket/%Y/%m/%d', default=None, blank=True, null=True,
                                   verbose_name='Дополнительные данные')
    date_uploaded = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заявки')

    class Meta:
        verbose_name = 'Заявку'
        verbose_name_plural = 'Заявки на помощь'
