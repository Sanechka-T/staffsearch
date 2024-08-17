from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class Contacts(TemplateView):
    template_name = 'info/contacts.html'
    extra_context = {
        'title': 'Контакты',
        'contacts_phone': '+7 (495) 987-65-43',
        'contacts_email': 'info@staffsearch.ru',
        'contacts_address': 'Димитровград, проспект Димитрова, 2А',
        'contacts_worktime': 'Ежедневно с 9:00 до 21:00',
    }
