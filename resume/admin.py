from django.contrib import admin

# Register your models here.
from .models import Resume, WorkExperience, Education, Portfolio, Photos, ProfessionalSkills, About


# Register your models here.

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    # Настройка административного интерфейса для модели Resume

    list_display = (
        'user', 'name', 'lastname', 'date_birth', 'city', 'removal',
        'remote_work', 'phone', 'email', 'post', 'salary',
        'employment', 'photo', 'resume_file', 'date_uploaded', 'date_update'
    )
    # Поля, которые будут отображаться в списке объектов модели Resume

    search_fields = (
        'name', 'lastname', 'city', 'email', 'post', 'salary'
    )
    # Поля, по которым можно искать объекты модели Resume в административном интерфейсе

    list_per_page = 5  # Количество объектов, отображаемых на одной странице


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = (
    'resume', 'position', 'company_name', 'start_date', 'end_date', 'experience', 'description', 'achievements',
    'right_now')
    search_fields = ('position', 'company_name', 'achievements')
    list_per_page = 5


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = (
    'resume', 'degree', 'form_of_education', 'year_of_graduation', 'educational_institution', 'faculty', 'specialty')
    search_fields = ('educational_institution', 'faculty', 'specialty')
    list_per_page = 5



@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('resume', 'description')
    search_fields = ('description',)
    list_per_page = 5


@admin.register(Photos)
class PhotosAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'image')
    list_per_page = 5


@admin.register(ProfessionalSkills)
class ProfessionalSkillsAdmin(admin.ModelAdmin):
    list_display = ('resume', 'skills')
    search_fields = ('skills',)
    list_per_page = 5


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('resume', 'biography')
    search_fields = ('biography',)
    list_per_page = 5
