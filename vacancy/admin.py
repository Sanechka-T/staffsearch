from django.contrib import admin
from .models import Vacancy, Conditions
# Register your models here.


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('company','title','profession','field_of_activity','description','photo','date_uploaded','date_update')
    search_fields = ('title','profession','description')
    list_per_page = 5


@admin.register(Conditions)
class ConditionsAdmin(admin.ModelAdmin):
    list_display = ('vacancy','employment','contract','salary','underworking','remote_work','frequency_payments','what_employees_get')
    search_fields = ('what_employees_get',)
    list_per_page = 5