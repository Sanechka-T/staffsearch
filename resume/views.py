import re
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DetailView

from staffsearch import settings
from .models import Resume, Photos
from .utils import DataMixin, ToolsMixin
from .forms import ResumeForm, WorkExperienceForm, EducationForm, AboutForm, ProfessionalSkillsForm, PortfolioForm


# Create your views here.


class ResumesHome(DataMixin, ListView):
    model = Resume

    def get_queryset(self):
        # Добавляем аннотацию к queryset
        return Resume.objects.all().select_related('professional_skills', 'about') \
                                   .prefetch_related('education', 'work_experience')


class ShowResume(LoginRequiredMixin, DetailView):
    model = Resume
    template_name = 'resume/resume.html'
    context_object_name = 'resume'
    extra_context = {
        'default_image': settings.DEFAULT_USER_IMAGE,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Резюме - {self.object.name} {self.object.lastname}"

        return context


@login_required(login_url='users:login')
def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        resume.delete()
        messages.success(request, 'Резюме успешно удалено.')
        return redirect('resumes')  # Перенаправление на список резюме
    data = {
        'title': 'Удаление резюме',
        'obj': resume
    }
    return render(request, 'confirm_delete.html', data)


@login_required(login_url='users:login')
def delete_resume_photo(request, photo_id):
    photo = get_object_or_404(Photos, id=photo_id, portfolio=request.user.resumes.first().portfolio)
    if request.method == 'POST':
        photo.delete()
        messages.success(request, 'Фото успешно удалено.')
        return redirect('resumes')  # Перенаправление на список резюме
    data = {
        'title': 'Удаление фото',
        'obj': photo
    }
    return render(request, 'confirm_delete.html', data)


@login_required(login_url='users:login')
def updateResume(request, resume_id):
    resume_info = get_object_or_404(Resume, id=resume_id, user=request.user)

    if request.method == 'POST':
        # Создаем формы с очищенными данными
        form_rf = ResumeForm(request.POST, instance=resume_info, prefix='resume')
        form_wef = WorkExperienceForm(request.POST, instance=resume_info.work_experience.first(),
                                      prefix='work_experience')
        form_ef = EducationForm(request.POST, instance=resume_info.education.first(), prefix='education')
        form_af = AboutForm(request.POST, instance=resume_info.about, prefix='about')
        form_psf = ProfessionalSkillsForm(request.POST, instance=resume_info.professional_skills, prefix='skills')
        form_pf = PortfolioForm(request.POST, instance=resume_info.portfolio, prefix='portfolio')

        # Проверяем валидность форм
        if all(form.is_valid() for form in [form_rf, form_wef, form_ef, form_af, form_psf, form_pf]):
            form_rf.save()
            form_wef.save()
            form_ef.save()
            form_af.save()
            form_psf.save()
            form_pf.save()
            images = request.FILES.getlist('images')
            for image in images:
                Photos.objects.create(
                    portfolio=form_pf,
                    image=image
                )
            return redirect('index')

    else:
        form_rf = ResumeForm(instance=resume_info, prefix='resume', initial={'salary': resume_info.salary.amount,
                                                                             'date_birth': str(resume_info.date_birth)})
        form_wef = WorkExperienceForm(instance=resume_info.work_experience.first(), prefix='work_experience',
                                      initial={'start_date': str(resume_info.work_experience.first().start_date),
                                               'end_date': str(resume_info.work_experience.first().end_date)})
        form_ef = EducationForm(instance=resume_info.education.first(), prefix='education')
        form_af = AboutForm(instance=resume_info.about, prefix='about')
        form_psf = ProfessionalSkillsForm(instance=resume_info.professional_skills, prefix='skills')
        form_pf = PortfolioForm(instance=resume_info.portfolio, prefix='portfolio')

    portfolio = resume_info.portfolio
    photos = portfolio.photos.all() if portfolio else []
    data = {
        'title': 'Редактирование резюме',
        'form_rf': form_rf,
        'form_wef': form_wef,
        'form_ef': form_ef,
        'form_af': form_af,
        'form_psf': form_psf,
        'form_pf': form_pf,
        'photos': photos,
    }
    return render(request, 'resume/createResume.html', context=data)


class SortResumes(DataMixin, ToolsMixin, ListView):
    template_name = 'resume/listResumes.html'
    context_object_name = 'resumes'

    def get_queryset(self):
        type_sort = self.request.GET.get('sort_field')
        if type_sort == 'sort_date':
            return Resume.objects.all().order_by('-date_update')
        elif type_sort == 'sort_age':
            return Resume.objects.all().order_by('date_birth')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_sort = self.request.GET.get('sort_field', '')
        context['type_sort'] = type_sort
        return context


class FilteringResumes(DataMixin, ToolsMixin, ListView):

    def get_queryset(self):
        queryset = Resume.objects.all()
        salary_min = self.request.GET.get('salary_min', '')
        salary_max = self.request.GET.get('salary_max', '')
        age_min = self.request.GET.get('age_min', '')
        age_max = self.request.GET.get('age_max', '')
        work_experience = self.request.GET.get('work_experience', '')
        employment_type = self.request.GET.get('employment_type', '')
        education_type = self.request.GET.get('education_type', '')

        if salary_min != '':
            queryset = queryset.filter(salary__gte=salary_min)
        if salary_max != '':
            queryset = queryset.filter(salary__lte=salary_max)
        if age_min != '':
            min_date_birth = date.today() - timedelta(days=int(age_min) * 365)
            queryset = queryset.filter(date_birth__lte=min_date_birth)
        if age_max != '':
            max_date_birth = date.today() - timedelta(days=int(age_max) * 365)
            queryset = queryset.filter(date_birth__gte=max_date_birth)
        if work_experience != '':
            queryset = queryset.filter(work_experience__experience=work_experience)
        if employment_type != '':
            queryset = queryset.filter(employment=employment_type)
        if education_type != '':
            queryset = queryset.filter(education__form_of_education=education_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['salary_min'] = self.request.GET.get('salary_min', '')
        context['salary_max'] = self.request.GET.get('salary_min', '')
        context['age_min'] = self.request.GET.get('age_min', '')
        context['age_max'] = self.request.GET.get('age_max', '')
        context['work_experience'] = self.request.GET.get('work_experience', '')
        context['employment_type'] = self.request.GET.get('employment_type', '')
        context['education_type'] = self.request.GET.get('education_type', '')
        return context


class SearchResumes(DataMixin, ToolsMixin, ListView):

    def get_queryset(self):
        return Resume.objects.filter(Q(post__icontains=self.request.GET.get('q')) |
                                     Q(professional_skills__skills__icontains=self.request.GET.get('q')))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')
        context['search_query'] = search_query
        return context


@login_required(login_url='users:login')
def createResume(request, *args, **kwargs):
    if request.method == 'POST':
        form_rf = ResumeForm(request.POST, prefix='resume')
        form_wef = WorkExperienceForm(request.POST, prefix='work_experience')
        form_ef = EducationForm(request.POST, prefix='education')
        form_af = AboutForm(request.POST, prefix='about')
        form_psf = ProfessionalSkillsForm(request.POST, prefix='skills')
        form_pf = PortfolioForm(request.POST, prefix='portfolio')
        if (form_rf.is_valid() and form_wef.is_valid() and
                form_ef.is_valid() and form_af.is_valid() and
                form_psf.is_valid() and form_pf.is_valid()):

            resume_info = form_rf.save(commit=False)
            resume_info.user = request.user
            resume_info.save()

            wef = form_wef.save(commit=False)
            wef.resume = resume_info
            wef.save()

            ef = form_ef.save(commit=False)
            ef.resume = resume_info
            ef.save()

            af = form_af.save(commit=False)
            af.resume = resume_info
            af.save()

            psf = form_psf.save(commit=False)
            psf.resume = resume_info
            psf.save()

            pf = form_pf.save(commit=False)
            pf.resume = resume_info
            pf.save()

            images = request.FILES.getlist('images')
            for image in images:
                Photos.objects.create(
                    portfolio=pf,
                    image=image
                )
            return redirect('index')
    else:
        form_rf = ResumeForm(prefix='resume')
        form_wef = WorkExperienceForm(prefix='work_experience')
        form_ef = EducationForm(prefix='education')
        form_af = AboutForm(prefix='about')
        form_psf = ProfessionalSkillsForm(prefix='skills')
        form_pf = PortfolioForm(prefix='portfolio')
    data = {
        'title': 'Создание резюме',
        'form_rf': form_rf,
        'form_wef': form_wef,
        'form_ef': form_ef,
        'form_af': form_af,
        'form_psf': form_psf,
        'form_pf': form_pf,
    }
    return render(request, 'resume/createResume.html', context=data)
