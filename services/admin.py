from django.contrib import admin
from .models import Service,Photos, Feedback, Additionally
# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('user','name','experience','group','description','price_list','cost','phone','email','date_uploaded','date_update')
    search_fields = ('name','description','price_list')
    list_per_page = 5


@admin.register(Photos)
class PhotosAdmin(admin.ModelAdmin):
    list_display = ('service','image')
    list_per_page = 5


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('service','estimation','feedback_text')
    list_per_page = 5


@admin.register(Additionally)
class AdditionallyAdmin(admin.ModelAdmin):
    list_display = ('service','contract','warranty','minimum_order','purchase','car','tools')
    list_per_page = 5

