from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField
from datetime import date


# Create your models here.


class Resume(models.Model):
    EMPLOYMENT_CHOICES = (
        ('full-time', 'Полная'),
        ('part-time', 'Частичная'),
        ('shift work', 'Вахтовая'),
        ('freelance', 'Фриланс'),
        ('temporary', 'Временная работа'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    name = models.CharField(max_length=50, verbose_name='Имя', blank=False)
    lastname = models.CharField(max_length=100, verbose_name='Фамилия', blank=False)
    date_birth = models.DateField(max_length=8, verbose_name='Дата рождения', blank=False)
    city = models.CharField(max_length=50, verbose_name='Город', blank=False)
    removal = models.BooleanField(default=False, verbose_name='Готовность к переезду', blank=True)
    remote_work = models.BooleanField(default=False, verbose_name='Удалённая работа', blank=True)
    phone = models.CharField(max_length=12, verbose_name='Телефон', blank=False)
    email = models.EmailField(max_length=100, verbose_name='Электронная почта', blank=False)
    post = models.CharField(max_length=100, verbose_name='Должность', blank=False )
    salary = MoneyField(max_digits=10, decimal_places=2, default_currency='RUB', verbose_name='Зарплата', blank=False)
    employment = models.CharField(max_length=10, choices=EMPLOYMENT_CHOICES, blank=False, default='full-time',
                                  verbose_name='Тип занятости')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d', default=None, blank=True, null=True)
    resume_file = models.FileField(upload_to='resume/%Y/%m/%d', default=None, blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания резюме')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления резюме')

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')

        # Проверка, что значение salary содержит только цифры
        if salary is not None:
            if not str(salary).isdigit():
                raise ValidationError("Поле 'Зарплата' должно содержать только цифры.")

        return salary

    def get_age(self):
        return (date.today() - self.date_birth).days // 365

    def get_true_age(self):
        age = self.get_age()
        suffix = "лет"
        if (age // 10) % 10 != 1:
            if age % 10 == 1:
                suffix = "год"
            elif age % 10 in (2, 3, 4) and not (age in [12, 13, 14]):
                suffix = "года"
        return f"{age} {suffix}"

    def __str__(self):
        return f"Резюме {self.post} {self.salary}"

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'


class WorkExperience(models.Model):
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
    resume = models.ForeignKey('Resume', on_delete=models.CASCADE, related_name='work_experience')
    position = models.CharField(max_length=100, verbose_name='Должность', blank=True, null=True)
    company_name = models.CharField(max_length=100, verbose_name='Название компании', blank=True, null=True)
    start_date = models.DateField(max_length=8, verbose_name='Дата начала работы', blank=True, null=True)
    end_date = models.DateField(max_length=8, verbose_name='Дата окончания работы', default=None, blank=True, null=True)
    right_now = models.BooleanField(default=0, verbose_name='По настоящее время', blank=True)
    experience = models.CharField(max_length=18, choices=EXPERIENCE_CHOICES, verbose_name='Стаж')
    description = models.TextField(verbose_name='Обязанности', default='', blank=True)
    achievements = models.TextField(verbose_name='Достижения', default='', blank=True)

    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыт работы'


class Education(models.Model):
    DEGREE_CHOICES = (
        ('doctor of science', 'Доктор наук'),
        ('candidate of sciences', 'Кандидат наук'),
        ('higher education', 'Высшее образование'),
        ('incomplete higher education', 'Неполное высшее образование'),
        ('secondary specialized education', 'Среднее специальное образование'),
        ('secondary education', 'Среднее образование'),
        ('bachelor', 'Бакалавр'),
        ('magister', 'Магистр'),
    )
    EDUCATION_CHOICES = (
        ('full-time', 'Очное'),
        ('evening', 'Вечернее'),
        ('full-part-time', 'Очно-заочное'),
        ('part-time', 'Заочное'),
        ('distance ', 'Дистанционное'),
    )
    resume = models.ForeignKey('Resume', on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=31, choices=DEGREE_CHOICES, verbose_name='Уровень образования')
    form_of_education = models.CharField(max_length=14, choices=EDUCATION_CHOICES, verbose_name='Форма обучения')
    year_of_graduation = models.PositiveIntegerField(validators=[MinValueValidator(1984)], verbose_name='Год окончания')
    educational_institution = models.CharField(max_length=100, verbose_name='Название учебного заведения')
    faculty = models.CharField(max_length=100, default='', blank=True, verbose_name='Факультет')
    specialty = models.CharField(max_length=150, default='', blank=True, verbose_name='Специальность')

    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образование'

class Portfolio(models.Model):
    resume = models.OneToOneField('Resume', on_delete=models.CASCADE, related_name='portfolio')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Портфолио'
        verbose_name_plural = 'Портфолио'


class Photos(models.Model):
    portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photo/resume_images/%Y/%m/%d', verbose_name='Фото для портфолио',
                              blank=True, null=True)

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Фотографии'


class ProfessionalSkills(models.Model):
    resume = models.OneToOneField('Resume', on_delete=models.CASCADE, related_name='professional_skills')
    skills = models.TextField(verbose_name='Навыки', blank=True, null=True)

    class Meta:
        verbose_name = 'Навыки'
        verbose_name_plural = 'Навыки'


class About(models.Model):
    resume = models.OneToOneField('Resume', on_delete=models.CASCADE, related_name='about')
    biography = models.TextField(verbose_name='Дополнительные сведения', blank=True, null=True)

    class Meta:
        verbose_name = 'Дополнительные сведения'
        verbose_name_plural = 'Дополнительные сведения'
