from django.urls import path
from . import views


app_name = 'help'

urlpatterns = [
    path('make-a-ticket/', views.MakeTicket.as_view(), name='makeTicket'),
]