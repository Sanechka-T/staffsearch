from django.urls import path
from . import views

urlpatterns = [
    path('create-service/', views.createService, name='createService'),
    path('service/<int:pk>/delete/', views.delete_service, name='delete_service'),
    path('service/<int:service_id>/feedback/', views.create_feedback, name='create_feedback'),
    path('services/', views.ListServices.as_view(), name='services'),
    path('service/<int:pk>/', views.ShowService.as_view(), name='showService'),
    path('sort-services/', views.SortServices.as_view(), name='sortServices'),
    path('filtering-services/', views.FilteringServices.as_view(), name='filteringServices'),
    path('search-services/', views.SearchServices.as_view(), name='searchServices'),
    path('update-service/<int:service_id>', views.updateService, name='updateService'),
    path('service/delete-photo/<int:photo_id>/', views.delete_service_photo, name='delete_service_photo'),
]