from django.shortcuts import redirect

from staffsearch import settings
from .models import WorkExperience, Resume, Education


class DataMixin:  # Класс-миксин для предоставления общих данных контекста для представлений.
    template_name = 'resume/listResumes.html'
    title_page = 'Поиск сотрудников и услуг, база резюме StaffSearch'
    extra_context = {  # Дополнительные контекстные данные для шаблона
        'sort_url': 'searchResumes',
        'sort_placeholder': 'Должность или навыки',
        'Experience': WorkExperience.EXPERIENCE_CHOICES,
        'Employment': Resume.EMPLOYMENT_CHOICES,
        'Education': Education.EDUCATION_CHOICES,
        'default_user_image': settings.DEFAULT_USER_IMAGE,
        'type_radio': 'resumes',
    }
    context_object_name = 'resumes'

    def __init__(self):  # Инициализация класса, установка заголовка страницы в extra_context.
        if self.title_page is not None:
            self.extra_context['title'] = self.title_page


class ToolsMixin:  # Миксин для добавления инструментов к представлениям.

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()  # Получение набора запросов.
        if queryset is None:  # Если результаты не найдены, перенаправление на страницу резюме.
            return redirect('resumes')
        return super().get(request, *args, **kwargs)  # Вызов родительского метода.
