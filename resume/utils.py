from django.shortcuts import redirect

from staffsearch import settings
from .models import WorkExperience, Resume, Education


class DataMixin:
    # paginate_by = 10
    template_name = 'resume/listResumes.html'
    title_page = 'Поиск сотрудников и услуг, база резюме StaffSearch'
    extra_context = {
        'sort_url': 'searchResumes',
        'sort_placeholder': 'Должность или навыки',
        'Experience': WorkExperience.EXPERIENCE_CHOICES,
        'Employment': Resume.EMPLOYMENT_CHOICES,
        'Education': Education.EDUCATION_CHOICES,
        'default_user_image': settings.DEFAULT_USER_IMAGE,
        'type_radio': 'resumes',
    }
    context_object_name = 'resumes'


    def __init__(self):
        if self.title_page is not None:
            self.extra_context['title'] = self.title_page


class ToolsMixin:

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return redirect('resumes')
        return super().get(request, *args, **kwargs)