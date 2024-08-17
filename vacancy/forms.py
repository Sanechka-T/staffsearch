from django import forms

from .models import Vacancy, Conditions


class VacancyForm(forms.ModelForm):
    title = forms.CharField(label='Название вакансии', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                     'placeholder': 'Например, "Срочно требуется сварщик 5 разряда"'}))

    profession = forms.CharField(label='Профессия', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                  'placeholder': 'Например, «Таргетолог» или «Электрик»'}))
    description = forms.CharField(label='Описание услуги',
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                                               'placeholder': 'Введите подробное описание вакансии...'}))

    field_of_activity = forms.CharField(label='Сфера деятельности',
                                        widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'Введите сферу деятельности...'}))
    photo = forms.ImageField(label='Логотип или фотография', required=False,
                             widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Vacancy
        fields = ('title', 'profession', 'field_of_activity', 'description', 'photo')


class ConditionsForm(forms.ModelForm):
    employment = forms.ChoiceField(label='Тип занятости', choices=Conditions.EMPLOYMENT_CHOICES,
                                   widget=forms.Select(attrs={'class': 'form-select'}))
    contract = forms.ChoiceField(label='Способ оформления', choices=Conditions.CONTRACT_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-select'}))
    salary = forms.DecimalField(label='Зарплата', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    underworking = forms.BooleanField(label='Подработка', required=False,
                                      widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    remote_work = forms.BooleanField(label='Удалённая работа', required=False,
                                     widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    frequency_payments = forms.ChoiceField(label='Частота выплат', choices=Conditions.FREQUENCY_CHOICES,
                                           widget=forms.Select(attrs={'class': 'form-select'}))
    what_employees_get = forms.CharField(label='Что получают работники', required=False,
                                         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                                                      'placeholder':
                                                                          'Например, Проживание, Питание, Обучение, Медицинская страховка и тд.'}))

    class Meta:
        model = Conditions
        fields = (
            'employment', 'contract', 'salary', 'underworking', 'remote_work', 'frequency_payments',
            'what_employees_get')
