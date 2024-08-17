from django.urls import path
from . import views

urlpatterns = [
    path('resumes/', views.ResumesHome.as_view(), name='resumes'),
    path('resume/<int:pk>/delete/', views.delete_resume, name='delete_resume'),
    path('resume/<int:pk>/', views.ShowResume.as_view(), name='showResume'),
    path('sort-resumes/', views.SortResumes.as_view(), name='sortResumes'),
    path('filtering-resumes/', views.FilteringResumes.as_view(), name='filteringResumes'),
    path('search-resumes/', views.SearchResumes.as_view(), name='searchResumes'),
    path('create-resume/', views.createResume, name='createResume'),
    path('update-resume/<int:resume_id>', views.updateResume, name='updateResume'),
    path('resume/<int:photo_id>/delete-photo/', views.delete_resume_photo, name='delete_resume_photo'),
]