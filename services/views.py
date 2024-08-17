from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Avg, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from .utils import DataMixin, ToolsMixin
from .models import Photos, Service
from .forms import ServiceForm, AdditionallyForm, FeedbackForm


# Create your views here.

@login_required(login_url='users:login')
def createService(request, *args, **kwargs):
    if request.method == 'POST':
        form_sf = ServiceForm(request.POST, prefix='service')
        form_af = AdditionallyForm(request.POST, prefix='additionally')

        if form_sf.is_valid() and form_af.is_valid():

            service_info = form_sf.save(commit=False)
            service_info.user = request.user
            service_info.save()

            additionally_info = form_af.save(commit=False)
            additionally_info.service = service_info
            additionally_info.save()

            images = request.FILES.getlist('images')
            for image in images:
                Photos.objects.create(
                    service=service_info,
                    image=image
                )
            return redirect('index')
    else:
        form_sf = ServiceForm(prefix='service')
        form_af = AdditionallyForm(prefix='additionally')
    data = {
        'title': 'Размещение услуги',
        'form_sf': form_sf,
        'form_af': form_af,
    }
    return render(request, 'services/createServices.html', context=data)


class ListServices(DataMixin, ListView):
    model = Service

    def get_queryset(self):
        # Добавляем аннотацию к queryset
        return Service.objects.annotate(feedback_count=Count('feedback'),average_rating=Avg('feedback__estimation'))


class ShowService(LoginRequiredMixin, DetailView):
    model = Service
    template_name = 'services/service.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Услуга - {self.object.name}"
        return context


@login_required(login_url='users:login')
def create_feedback(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.service = service
            feedback.save()
            return redirect('showService', pk=service.id)
    else:
        form = FeedbackForm()

    return render(request, 'services/createFeedback.html', {'form': form, 'service': service})


@login_required(login_url='users:login')
def delete_service_photo(request, photo_id):
    photo = get_object_or_404(Photos, id=photo_id)
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
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk, user=request.user)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Услуга успешно удалена.')
        return redirect('services')
    data = {
        'title': 'Удаление услуги',
        'obj': service
    }
    return render(request, 'confirm_delete.html', data)


@login_required(login_url='users:login')
def updateService(request, service_id):
    service_info = get_object_or_404(Service, id=service_id, user=request.user)

    if request.method == 'POST':
        # Создаем формы с очищенными данными
        form_sf = ServiceForm(request.POST, instance=service_info, prefix='service')
        form_af = AdditionallyForm(request.POST, instance=service_info.additionally, prefix='additionally')

        # Проверяем валидность форм
        if all(form.is_valid() for form in [form_sf, form_af]):
            form_sf.save()
            form_af.save()
            images = request.FILES.getlist('images')
            for image in images:
                Photos.objects.create(
                    service=service_info,
                    image=image
                )
            return redirect('index')

    else:
        form_sf = ServiceForm(instance=service_info, prefix='service', initial={'cost': service_info.cost.amount})
        form_af = AdditionallyForm(instance=service_info.additionally, prefix='additionally', initial={'minimum_order': service_info.additionally.minimum_order.amount})

    photos = service_info.photos.all() if service_info.photos else []
    data = {
        'title': 'Редактирование услуги',
        'form_sf': form_sf,
        'form_af': form_af,
        'photos': photos,
    }
    return render(request, 'services/createServices.html', context=data)


class SortServices(DataMixin, ToolsMixin, ListView):

    def get_queryset(self):
        type_sort = self.request.GET.get('sort_field')
        if type_sort == 'sort_exp':
            return Service.objects.all().order_by('-experience')
        elif type_sort == 'sort_cost':
            return Service.objects.all().order_by('cost')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_sort = self.request.GET.get('sort_field', '')
        context['type_sort'] = type_sort
        return context


class FilteringServices(DataMixin, ToolsMixin, ListView):

    def get_queryset(self):
        queryset = Service.objects.all()
        cost_min = self.request.GET.get('cost_min', '')
        cost_max = self.request.GET.get('cost_max', '')
        estimation_min = self.request.GET.get('estimation_min', '')
        estimation_max = self.request.GET.get('estimation_max', '')
        work_experience = self.request.GET.get('work_experience', '')
        contract = self.request.GET.get('contract', '')
        warranty = self.request.GET.get('warranty', '')
        car = self.request.GET.get('car', '')
        tools = self.request.GET.get('tools', '')

        if cost_min != '':
            queryset = queryset.filter(cost__gte=cost_min)
        if cost_max != '':
            queryset = queryset.filter(cost__lte=cost_max)
        if estimation_min != '':
            queryset.annotate(average_rating=Avg('feedback__estimation'))
            queryset = queryset.filter(average_rating__gte=estimation_min)
        if estimation_max != '':
            queryset.annotate(average_rating=Avg('feedback__estimation'))
            queryset = queryset.filter(average_rating__lte=estimation_max)
        if work_experience != '':
            queryset = queryset.filter(experience=work_experience)
        if contract != '':
            queryset = queryset.filter(additionally__contract=contract)
        if warranty != '':
            queryset = queryset.filter(additionally__warranty=warranty)
        if car != '':
            queryset = queryset.filter(additionally__car=car)
        if tools != '':
            queryset = queryset.filter(additionally__tools=tools)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cost_min'] = self.request.GET.get('cost_min', '')
        context['cost_max'] = self.request.GET.get('cost_max', '')
        context['estimation_min'] = self.request.GET.get('estimation_min', '')
        context['estimation_max'] = self.request.GET.get('estimation_max', '')
        context['work_experience'] = self.request.GET.get('work_experience', '')
        context['contract'] = self.request.GET.get('contract', '')
        context['warranty'] = self.request.GET.get('warranty', '')
        context['car'] = self.request.GET.get('car', '')
        context['tools'] = self.request.GET.get('tools', '')
        return context


class SearchServices(DataMixin, ToolsMixin, ListView):

    def get_queryset(self):
        return Service.objects.filter(Q(name__icontains=self.request.GET.get('q')) |
                                      Q(price_list__icontains=self.request.GET.get('q'))
                                      | Q(description__icontains=self.request.GET.get('q')))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')
        context['search_query'] = search_query
        return context
