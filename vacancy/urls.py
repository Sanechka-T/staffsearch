from django.urls import path
from . import views

urlpatterns = [
    path('create-vacancy/', views.createVacancy, name='createVacancy'),
    path('vacancy/<int:pk>/delete/', views.delete_vacancy, name='delete_vacancy'),
    path('vacancies/', views.ListVacancies.as_view(), name='vacancies'),
    path('vacancy/<int:pk>/', views.ShowVacancy.as_view(), name='showVacancy'),
    path('sort-vacancies/', views.SortVacancies.as_view(), name='sortVacancies'),
    path('filtering-vacancies/', views.FilteringVacancies.as_view(), name='filteringVacancies'),
    path('search-vacancies/', views.SearchVacancies.as_view(), name='searchVacancies'),
    path('update-vacancy/<int:vacancy_id>', views.updateVacancy, name='updateVacancy'),
]