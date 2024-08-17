from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import MakeTicketForm


# Create your views here.
class MakeTicket(CreateView):
    form_class = MakeTicketForm
    template_name = 'help/makeTicket.html'
    extra_context = {
        'title': 'Служба поддержки StaffSearch'
    }
    success_url = reverse_lazy('index')

