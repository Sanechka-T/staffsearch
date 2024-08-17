from django import forms
from .models import Ticket


class MakeTicketForm(forms.ModelForm):
    title = forms.ChoiceField(label='Тема обращения',choices=Ticket.TICKET_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Ваш номер телефона',
                                                                           'id': 'phone'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Ваш вопрос', required=False,
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5,
                                                               'placeholder':
                                                                   'Опишите во всех подробностях вашу проблему...'}))
    ticket_file = forms.FileField(label='Картинка jpeg или документ Word', required=False,
                                  widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Ticket
        fields = ('title', 'phone', 'email', 'description', 'ticket_file')
