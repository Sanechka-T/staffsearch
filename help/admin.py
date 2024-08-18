from django.contrib import admin
from .models import Ticket
# Register your models here.

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'email', 'description', 'ticket_file','date_uploaded')
    search_fields = ['title', 'phone', 'email']
    list_per_page = 5