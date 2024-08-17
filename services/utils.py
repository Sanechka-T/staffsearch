from django.shortcuts import redirect

from staffsearch import settings
from .models import Service, Additionally


class DataMixin:
    # paginate_by = 10
    title_page = 'Поиск сотрудников и услуг, база резюме StaffSearch'
    template_name = 'services/listServices.html'
    context_object_name = 'services'
    extra_context = {
        'sort_url': 'searchServices',
        'sort_placeholder': 'Например: парикмахер, уборка, сантехник...',
        'Experience': Service.EXPERIENCE_CHOICES,
        'default_image': settings.DEFAULT_IMAGE,
        'type_radio': 'services',
    }

    def __init__(self):
        if self.title_page is not None:
            self.extra_context['title'] = self.title_page


class ToolsMixin:

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return redirect('services')
        return super().get(request, *args, **kwargs)