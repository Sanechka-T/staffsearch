from django.urls import path
from . import views

urlpatterns = [
    # Путь к главной странице резюме
    path('resumes/', views.ResumesHome.as_view(), name='resumes'),

    # Путь для удаления резюме по его первичному ключу (pk)
    path('resume/<int:pk>/delete/', views.delete_resume, name='delete_resume'),

    # Путь для отображения резюме по его первичному ключу (pk)
    path('resume/<int:pk>/', views.ShowResume.as_view(), name='showResume'),

    # Путь для сортировки резюме
    path('sort-resumes/', views.SortResumes.as_view(), name='sortResumes'),

    # Путь для фильтрации резюме
    path('filtering-resumes/', views.FilteringResumes.as_view(), name='filteringResumes'),

    # Путь для поиска резюме
    path('search-resumes/', views.SearchResumes.as_view(), name='searchResumes'),

    # Путь для создания нового резюме
    path('create-resume/', views.createResume, name='createResume'),

    # Путь для обновления резюме по ID резюме
    path('update-resume/<int:resume_id>', views.updateResume, name='updateResume'),

    # Путь для удаления фотографии резюме по ID фотографии
    path('resume/<int:photo_id>/delete-photo/', views.delete_resume_photo, name='delete_resume_photo'),
]
