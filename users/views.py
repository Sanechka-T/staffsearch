import json

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView

from staffsearch import settings
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, RegisterEmployerForm


# Create your views here.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


class RegisterUser(View):
    def get(self, request):
        form_ruf = RegisterUserForm(prefix='register_user')
        data = {
            'form_ruf': form_ruf,
            'title': "Регистрация",
        }
        return render(request, 'users/registration.html', data)

    def post(self, request):
        form_ruf = RegisterUserForm(request.POST, prefix='register_user')
        data = {
            'form_ruf': form_ruf,
            'title': "Регистрация",
        }
        if form_ruf.is_valid():
            obj_user = form_ruf.save()
            if 'reg_company' in request.POST:
                request.session['user_data'] = json.dumps({'id': obj_user.id,})
                return redirect('users:register_company')
            else:
                return redirect('users:register_done')
        return render(request, 'users/registration.html', data)


class RegisterEmployer(View):
    def get(self, request):
        user_data = json.loads(request.session.get('user_data', '{}'))
        if len(user_data) == 0:
            return HttpResponseForbidden()
        form_ref = RegisterEmployerForm(prefix='register_employer')
        data = {
            'form_ref': form_ref,
            'title': "Регистрация для работодателя",
        }
        return render(request, 'users/registration_employer.html', data)

    def post(self, request):
        form_ref = RegisterEmployerForm(request.POST, prefix='register_employer')
        if form_ref.is_valid():
            company = form_ref.save(commit=False)
            user_data = json.loads(request.session.get('user_data', '{}'))
            company.user = get_user_model().objects.get(id=user_data['id'])
            company.save()
            return redirect('users:register_done')


class RegisterDone(TemplateView):
    template_name = 'users/register_done.html'
    extra_context = {'title': 'Регистрация завершена'}


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {
        'title': "Профиль пользователя",
        'default_user_image': settings.DEFAULT_USER_IMAGE,
        'default_image': settings.DEFAULT_IMAGE,
    }

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
