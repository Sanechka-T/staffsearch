from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('register_company/', views.RegisterEmployer.as_view(), name='register_company'),
    path('register_done/', views.RegisterDone.as_view(), name='register_done'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
]