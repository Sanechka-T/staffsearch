from staffsearch import settings
from .models import Conditions
from django.shortcuts import redirect


class DataMixin:
    # paginate_by = 10
    title_page = 'Поиск сотрудников и услуг, база резюме StaffSearch'
    template_name = 'vacancy/listVacancies.html'
    context_object_name = 'vacancies'
    extra_context = {
        'sort_url': 'searchVacancies',
        'sort_placeholder': 'Например: разработчик, маркетолог, менеджер проекта...',
        'Employment': Conditions.EMPLOYMENT_CHOICES,
        'Contract': Conditions.CONTRACT_CHOICES,
        'Frequency': Conditions.FREQUENCY_CHOICES,
        'default_image': settings.DEFAULT_IMAGE,
        'type_radio': 'vacancies',
    }

    def __init__(self):
        if self.title_page is not None:
            self.extra_context['title'] = self.title_page


class ToolsMixin:

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return redirect('vacancies')
        return super().get(request, *args, **kwargs)