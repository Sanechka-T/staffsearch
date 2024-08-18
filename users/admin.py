from django.contrib import admin
from .models import Employer
# Register your models here.


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('user','company_name','company_description','company_phone','company_email','company_address','company_site')
    search_fields = ('name','company_name','company_description')
    list_per_page = 5
