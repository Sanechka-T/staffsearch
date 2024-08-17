from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from .forms import VacancyForm, ConditionsForm
from .models import Vacancy
from .utils import DataMixin, ToolsMixin


@login_required(login_url='users:login')
def createVacancy(request, *args, **kwargs):
    if request.method == 'POST':
        form_vf = VacancyForm(request.POST, prefix='vacancy')
        form_cf = ConditionsForm(request.POST, prefix='conditions')

        if form_vf.is_valid() and form_cf.is_valid():
            vacancy_info = form_vf.save(commit=False)
            vacancy_info.company = request.user.employer
            vacancy_info.save()

            conditions_info = form_cf.save(commit=False)
            conditions_info.vacancy = vacancy_info
            conditions_info.save()

            return redirect('vacancies')
    else:
        form_vf = VacancyForm(prefix='vacancy')
        form_cf = ConditionsForm(prefix='conditions')
    data = {
        'title': 'Размещение вакансии',
        'form_vf': form_vf,
        'form_cf': form_cf,
    }
    return render(request, 'vacancy/createVacancy.html', context=data)


class ListVacancies(DataMixin, ListView):
    model = Vacancy

    def get_queryset(self):
        # Добавляем аннотацию к queryset
        return Vacancy.objects.all().select_related('conditions')


@login_required(login_url='users:login')
def delete_vacancy(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk, company=request.user.employer)
    if request.method == 'POST':
        vacancy.delete()
        messages.success(request, 'Вакансия успешно удалена.')
        return redirect('vacancies')
    data = {
        'title': 'Удаление вакансии',
        'obj': vacancy
    }
    return render(request, 'confirm_delete.html', data)


class ShowVacancy(LoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = 'vacancy/vacancy.html'
    context_object_name = 'vacancy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Вакансия - {self.object.title}"
        return context


@login_required(login_url='users:login')
def updateVacancy(request, vacancy_id):
    vacancy_info = get_object_or_404(Vacancy, id=vacancy_id, company=request.user.employer)

    if request.method == 'POST':
        # Создаем формы с очищенными данными
        form_vf = VacancyForm(request.POST, instance=vacancy_info, prefix='vacancy')
        form_cf = ConditionsForm(request.POST, instance=vacancy_info.conditions, prefix='conditions')

        # Проверяем валидность форм
        if all(form.is_valid() for form in [form_vf, form_cf]):
            form_vf.save()
            form_cf.save()
            return redirect('index')

    else:
        form_vf = VacancyForm(instance=vacancy_info, prefix='vacancy')
        form_cf = ConditionsForm(instance=vacancy_info.conditions, prefix='conditions', initial={'salary': vacancy_info.conditions.salary.amount})

    photo = vacancy_info.photo
    data = {
        'title': 'Редактирование вакансии',
        'form_vf': form_vf,
        'form_cf': form_cf,
        'photo': photo,
    }
    return render(request, 'vacancy/createVacancy.html', context=data)


class SortVacancies(DataMixin, ToolsMixin, ListView):

    def get_queryset(self):
        type_sort = self.request.GET.get('sort_field')
        if type_sort == 'sort_data':
            return Vacancy.objects.all().order_by('-date_update')
        elif type_sort == 'sort_salary':
            return Vacancy.objects.all().order_by('-conditions__salary')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_sort = self.request.GET.get('sort_field', '')
        context['type_sort'] = type_sort
        return context


class FilteringVacancies(DataMixin, ToolsMixin, ListView):

    def get_queryset(self):
        queryset = Vacancy.objects.all()
        salary_min = self.request.GET.get('salary_min', '')
        salary_max = self.request.GET.get('salary_max', '')
        employment = self.request.GET.get('employment', '')
        contract = self.request.GET.get('contract', '')
        frequency = self.request.GET.get('frequency', '')
        underworking = self.request.GET.get('underworking', '')
        remote_work = self.request.GET.get('remote_work', '')

        if salary_min != '':
            queryset = queryset.filter(conditions__salary__gte=salary_min)
        if salary_max != '':
            queryset = queryset.filter(conditions__salary__lte=salary_max)
        if employment != '':
            queryset = queryset.filter(conditions__employment=employment)
        if contract != '':
            queryset = queryset.filter(conditions__contract=contract)
        if frequency != '':
            queryset = queryset.filter(conditions__frequency_payments=frequency)
        if underworking != '':
            queryset = queryset.filter(conditions__underworking=underworking)
        if remote_work != '':
            queryset = queryset.filter(conditions__remote_work=remote_work)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['salary_min'] = self.request.GET.get('salary_min', '')
        context['salary_max'] = self.request.GET.get('salary_max', '')
        context['employment'] = self.request.GET.get('employment', '')
        context['contract'] = self.request.GET.get('contract', '')
        context['frequency'] = self.request.GET.get('frequency', '')
        context['underworking'] = self.request.GET.get('underworking', '')
        context['remote_work'] = self.request.GET.get('remote_work', '')
        return context


class SearchVacancies(DataMixin, ToolsMixin, ListView):

    def get_queryset(self):
        return Vacancy.objects.filter(Q(title__icontains=self.request.GET.get('q')) |
                                      Q(profession__icontains=self.request.GET.get('q'))
                                      | Q(field_of_activity__icontains=self.request.GET.get('q'))
                                      | Q(description__icontains=self.request.GET.get('q')))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')
        context['search_query'] = search_query
        return context
