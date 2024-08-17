import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Employer


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин",
                               widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(
        max_length=25,
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        max_length=25,
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'})
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Логин'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class RegisterEmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'company_description', 'company_phone', 'company_email', 'company_address',
                  'company_site']
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'Название компании'}),
            'company_description': forms.TextInput(attrs={'placeholder': 'Описание компании'}),
            'company_phone': forms.TextInput(attrs={'placeholder': 'Телефон компании'}),
            'company_email': forms.TextInput(attrs={'placeholder': 'Email компании'}),
            'company_address': forms.TextInput(attrs={'placeholder': 'Адрес компании'}),
            'company_site': forms.TextInput(attrs={'placeholder': 'Сайт компании'}),
        }



class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-control'}))  # disabled=True запрет на изменение полей
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
