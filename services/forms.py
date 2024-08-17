from django import forms

from .models import Service, Additionally, Feedback


class ServiceForm(forms.ModelForm):
    name = forms.CharField(label='Название услуги', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                   'placeholder':'Например, «Мастер плиточник» или «Ремонт квартир под ключ»'}))
    experience = forms.ChoiceField(label='Опыт работы', choices=Service.EXPERIENCE_CHOICES,
                                   widget=forms.Select(attrs={'class': 'form-select'}))
    group = forms.ChoiceField(label='Каким составом работаете', choices=Service.GROUP_CHOICES,
                              widget=forms.Select(attrs={'class': 'form-select'}))

    description = forms.CharField(label='Описание услуги',
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                                               'placeholder':'Введите подробное описание услуги, включая основные характеристики и преимущества...'}))
    price_list = forms.CharField(label='Прайс-лист', required=False,
                                 widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                                               'placeholder':'Введите стоимость услуги, а также возможные скидки и дополнительные опции...'}))
    cost = forms.DecimalField(label='Стоимость основной услуги',
                              widget=forms.NumberInput(attrs={'class': 'form-control',
                                                              'placeholder':'₽'}))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Укажите номер телефона для связи'}))

    email = forms.EmailField(label='Почта', required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Service
        fields = (
            'name', 'experience', 'group', 'description', 'price_list', 'cost', 'phone', 'email')


class AdditionallyForm(forms.ModelForm):
    contract = forms.ChoiceField(label='Работа по договору', choices=Additionally.CONTRACT_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-select'}))
    warranty = forms.ChoiceField(label='Гарантия на работу', choices=Additionally.WARRANTY_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-select'}))
    minimum_order = forms.DecimalField(label='Минимальная сумма заказа', required=False,
                                       widget=forms.NumberInput(attrs={'class': 'form-control'}))
    purchase = forms.ChoiceField(label='Закупка материалов', choices=Additionally.PURCHASE_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-select'}))
    car = forms.ChoiceField(label='Транспортное средство', choices=Additionally.WARRANTY_CHOICES,
                            widget=forms.Select(attrs={'class': 'form-select'}))
    tools = forms.ChoiceField(label='Свои инструменты', choices=Additionally.CONTRACT_CHOICES,
                              widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Additionally
        fields = (
            'contract', 'warranty', 'minimum_order', 'purchase', 'car', 'tools')


class FeedbackForm(forms.ModelForm):
    # estimation = forms.ChoiceField(label='Оценка', choices=Feedback.ESTIMATION_CHOICES,
    #                                widget=forms.Select(attrs={'class': 'form-control'}))
    feedback_text = forms.CharField(label='Отзыв',
                                    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                                                 'placeholder': 'Расскажите как всё прошло...'}))

    class Meta:
        model = Feedback
        fields = (
            'estimation', 'feedback_text')
