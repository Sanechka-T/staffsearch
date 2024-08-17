from django.urls import path
from . import views

app_name = "info"

urlpatterns = [
    path('contacts/', views.Contacts.as_view(), name='contacts'),
]